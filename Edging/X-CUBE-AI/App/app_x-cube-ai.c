
/**
  ******************************************************************************
  * @file    app_x-cube-ai.c
  * @author  X-CUBE-AI C code generator
  * @brief   AI program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */

 /*
  * Description
  *   v1.0 - Minimum template to show how to use the Embedded Client API
  *          model. Only one input and one output is supported. All
  *          memory resources are allocated statically (AI_NETWORK_XX, defines
  *          are used).
  *          Re-target of the printf function is out-of-scope.
  *   v2.0 - add multiple IO and/or multiple heap support
  *
  *   For more information, see the embeded documentation:
  *
  *       [1] %X_CUBE_AI_DIR%/Documentation/index.html
  *
  *   X_CUBE_AI_DIR indicates the location where the X-CUBE-AI pack is installed
  *   typical : C:\Users\[user_name]\STM32Cube\Repository\STMicroelectronics\X-CUBE-AI\7.1.0
  */

#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/

#if defined ( __ICCARM__ )
#elif defined ( __CC_ARM ) || ( __GNUC__ )
#endif

/* System headers */
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "app_x-cube-ai.h"
#include "main.h"
#include "ai_datatypes_defines.h"
#include "cnn_2d_edging_ai.h"
#include "cnn_2d_edging_ai_data.h"

/* USER CODE BEGIN includes */
#include "53l8a1_ranging_sensor.h"
extern __IO uint32_t ToF_EventFlag;
/* USER CODE END includes */

/* IO buffers ----------------------------------------------------------------*/

#if !defined(AI_CNN_2D_EDGING_AI_INPUTS_IN_ACTIVATIONS)
AI_ALIGNED(4) ai_i8 data_in_1[AI_CNN_2D_EDGING_AI_IN_1_SIZE_BYTES];
ai_i8* data_ins[AI_CNN_2D_EDGING_AI_IN_NUM] = {
data_in_1
};
#else
ai_i8* data_ins[AI_CNN_2D_EDGING_AI_IN_NUM] = {
NULL
};
#endif

#if !defined(AI_CNN_2D_EDGING_AI_OUTPUTS_IN_ACTIVATIONS)
AI_ALIGNED(4) ai_i8 data_out_1[AI_CNN_2D_EDGING_AI_OUT_1_SIZE_BYTES];
ai_i8* data_outs[AI_CNN_2D_EDGING_AI_OUT_NUM] = {
data_out_1
};
#else
ai_i8* data_outs[AI_CNN_2D_EDGING_AI_OUT_NUM] = {
NULL
};
#endif

/* Activations buffers -------------------------------------------------------*/

AI_ALIGNED(32)
static uint8_t pool0[AI_CNN_2D_EDGING_AI_DATA_ACTIVATION_1_SIZE];

ai_handle data_activations0[] = {pool0};

/* AI objects ----------------------------------------------------------------*/

static ai_handle cnn_2d_edging_ai = AI_HANDLE_NULL;

static ai_buffer* ai_input;
static ai_buffer* ai_output;

static void ai_log_err(const ai_error err, const char *fct)
{
  /* USER CODE BEGIN log */
  if (fct)
    printf("TEMPLATE - Error (%s) - type=0x%02x code=0x%02x\r\n", fct,
        err.type, err.code);
  else
    printf("TEMPLATE - Error - type=0x%02x code=0x%02x\r\n", err.type, err.code);

  do {} while (1);
  /* USER CODE END log */
}

static int ai_boostrap(ai_handle *act_addr)
{
  ai_error err;

  /* Create and initialize an instance of the model */
  err = ai_cnn_2d_edging_ai_create_and_init(&cnn_2d_edging_ai, act_addr, NULL);
  if (err.type != AI_ERROR_NONE) {
    ai_log_err(err, "ai_cnn_2d_edging_ai_create_and_init");
    return -1;
  }

  ai_input = ai_cnn_2d_edging_ai_inputs_get(cnn_2d_edging_ai, NULL);
  ai_output = ai_cnn_2d_edging_ai_outputs_get(cnn_2d_edging_ai, NULL);

#if defined(AI_CNN_2D_EDGING_AI_INPUTS_IN_ACTIVATIONS)
  /*  In the case where "--allocate-inputs" option is used, memory buffer can be
   *  used from the activations buffer. This is not mandatory.
   */
  for (int idx=0; idx < AI_CNN_2D_EDGING_AI_IN_NUM; idx++) {
	data_ins[idx] = ai_input[idx].data;
  }
#else
  for (int idx=0; idx < AI_CNN_2D_EDGING_AI_IN_NUM; idx++) {
	  ai_input[idx].data = data_ins[idx];
  }
#endif

#if defined(AI_CNN_2D_EDGING_AI_OUTPUTS_IN_ACTIVATIONS)
  /*  In the case where "--allocate-outputs" option is used, memory buffer can be
   *  used from the activations buffer. This is no mandatory.
   */
  for (int idx=0; idx < AI_CNN_2D_EDGING_AI_OUT_NUM; idx++) {
	data_outs[idx] = ai_output[idx].data;
  }
#else
  for (int idx=0; idx < AI_CNN_2D_EDGING_AI_OUT_NUM; idx++) {
	ai_output[idx].data = data_outs[idx];
  }
#endif

  return 0;
}

static int ai_run(void)
{
  ai_i32 batch;

  batch = ai_cnn_2d_edging_ai_run(cnn_2d_edging_ai, ai_input, ai_output);
  if (batch != 1) {
    ai_log_err(ai_cnn_2d_edging_ai_get_error(cnn_2d_edging_ai),
        "ai_cnn_2d_edging_ai_run");
    return -1;
  }

  return 0;
}

/* USER CODE BEGIN 2 */
int acquire_and_process_data(ai_i8* data[])
{
    /* Pobierz dane z czujnika ToF VL53L8CX
     * Czujnik mierzy 64 strefy (siatka 8x8)
     * Dla każdej strefy pobieramy:
     *   - Distance[0] = odległość w mm (0-2000)
     *   - Signal[0]   = siła sygnału
     * Łącznie 128 liczb = wejście do modelu AI */

    RANGING_SENSOR_Result_t Result;
    int32_t status = -1;

    if (ToF_EventFlag)  /* Czy czujnik ma nowe dane? */
    {
        ToF_EventFlag = RESET;  /* Zaznacz że odczytaliśmy */
        status = VL53L8A1_RANGING_SENSOR_GetDistance(
                     VL53L8A1_DEV_CENTER, &Result);

        if (status == BSP_ERROR_NONE)
        {
            float* input = (float*)data[0];  /* Bufor wejściowy modelu */
            int j = 0;

            for (int i = 0; i < 64; i++)  /* Dla każdej z 64 stref */
            {
                /* Odległość - ogranicz do 2000mm */
                if (Result.ZoneResult[i].Distance[0] <= 2000)
                    input[j++] = (float)Result.ZoneResult[i].Distance[0];
                else
                    input[j++] = 2000.0f;

                /* Siła sygnału */
                input[j++] = (float)Result.ZoneResult[i].Signal[0];
            }
            return 0;  /* Sukces - dane gotowe dla AI */
        }
    }
    return -1;  /* Brak nowych danych - poczekaj na następny pomiar */
}

int post_process(ai_i8* data[])
{
    /* Przetwórz wynik modelu AI
     * Model zwraca 8 liczb (pewność dla każdego gestu)
     * Wybieramy gest z największą pewnością
     * i wysyłamy jego nazwę przez UART */

    float* output = (float*)data[0];

    /* Nazwy gestów - kolejność musi zgadzać się z modelem!
     * Model: st_cnn2d_handposture_8classes z STM32 Model Zoo */
    const char* gesty[] = {
        "NONE",       /* 0 - brak gestu */
        "FLAT_HAND",  /* 1 - płaska dłoń */
        "LIKE",       /* 2 - kciuk w górę */
        "DISLIKE",    /* 3 - kciuk w dół */
        "FIST",       /* 4 - pięść */
        "LOVE",       /* 5 - kocham cię */
        "BREAKTIME",  /* 6 - przerwa */
        "CROSSHANDS"  /* 7 - skrzyżowane dłonie */
    };

    /* Znajdź gest z największą pewnością */
    int max_index = 0;
    float max_value = output[0];

    for (int i = 1; i < 8; i++)
    {
        if (output[i] > max_value)
        {
            max_value = output[i];
            max_index = i;
        }
    }

    /* Wyślij przez UART - skrypt Python to odbierze */
    printf("GEST:%s\r\n", gesty[max_index]);
    return 0;
}
/* USER CODE END 2 */

/* Entry points --------------------------------------------------------------*/

void MX_X_CUBE_AI_Init(void)
{
    /* USER CODE BEGIN 5 */
  printf("\r\nTEMPLATE - initialization\r\n");

  ai_boostrap(data_activations0);
    /* USER CODE END 5 */
}

void MX_X_CUBE_AI_Process(void)
{
    /* USER CODE BEGIN 6 */
  int res = -1;

  printf("TEMPLATE - run - main loop\r\n");

  if (cnn_2d_edging_ai) {

    do {
      /* 1 - acquire and pre-process input data */
      res = acquire_and_process_data(data_ins);
      /* 2 - process the data - call inference engine */
      if (res == 0)
        res = ai_run();
      /* 3- post-process the predictions */
      if (res == 0)
        res = post_process(data_outs);
    } while (res==0);
  }

  if (res) {
    ai_error err = {AI_ERROR_INVALID_STATE, AI_ERROR_CODE_NETWORK};
    ai_log_err(err, "Process has FAILED");
  }
    /* USER CODE END 6 */
}
#ifdef __cplusplus
}
#endif
