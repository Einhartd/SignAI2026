
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
//#define FIXED_POINT_14_2_TO_FLOAT                 (4.0)
//#define FIXED_POINT_21_11_TO_FLOAT                (2048.0)
#include <stdbool.h>
//extern RANGING_SENSOR_Result_t ToF_Data;
//HANDPOSTURE_converted_data Ranging_converted_data;
//RANGING_SENSOR_ZoneResult_t Data_ToF;
 uint32_t five_counter = 0;
 extern float ai_data_input[128];
 extern float ai_data_output[8];
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
/* USER CODE BEGIN 2 */
//int acquire_and_process_data(ai_i8* data[], RANGING_SENSOR_Result_t* ToF_Data)
//{
//	// PLAN NA PREPROCESSING
//	// 1. Zapisanie znacznika czasu
//	// 2. Walidacja odczytu z czujnika (czy nie ma bledu)
//	// 3. Skopiowanie danych do nowej struktury
//	// 4. Zamiana danych ze staloprzecinkowych na zmienno
//	// 5. Sprawdzenie poprawności odczytu (np. czy odległość mieści się w rozsądnym zakresie)
//	// 6. Pętla maskująca (Background removal)
//	// TUTAJ POWINIEN BYC WYCZYSZCZONY ODCZYT
//	// 7. Normalizacja danych (standaryzacja / IQR)
//	// 8. Ulozenie do bufora wejsciowego AI
//	// sprawdzic siec
//	// KONIEC PREPROCESSINGU
//
//
//
//  // Rzutujemy uniwersalny bufor na wskaźnik float
//  float *ai_input_buffer = (float *)data[0];
//
//  // --- STAŁE Z PROJEKTU REFERENCYJNEGO ST ---
//  const float NORM_RANGING_CENTER = 295.0f;
//  const float NORM_RANGING_IQR    = 196.0f;
//  const float NORM_SIGNAL_CENTER  = 281.0f;
//  const float NORM_SIGNAL_IQR     = 452.0f;
//  const float DEFAULT_RANGING     = 4000.0f;
//  const float DEFAULT_SIGNAL      = 0.0f;
//
//  for (int i = 0; i < 64; i++)
//  {
//      float distance_f = 0.0f;
//      float signal_f = 0.0f;
//
//      // 1. WALIDACJA ODCZYTU Z CZUJNIKA
//      uint8_t targets = ToF_Data.ZoneResult[i].NumberOfTargets;
//      uint8_t status = ToF_Data.ZoneResult[i].Status[0];
//
//      // Akceptujemy tylko statusy 5 oraz 9
//      if ((targets > 0) && (status == 5 || status == 9))
//      {
//          // 2. DEKODOWANIE FORMATU FIXED-POINT
//          distance_f = (float)ToF_Data.ZoneResult[i].Distance[0] / 4.0f;     // Format 14.2
//          signal_f   = (float)ToF_Data.ZoneResult[i].Signal[0] / 2048.0f;    // Format 21.11
//      }
//      else
//      {
//          // Wypełnianie tła (Background removal)
//          distance_f = DEFAULT_RANGING;
//          signal_f   = DEFAULT_SIGNAL;
//      }
//
//      // 3. NORMALIZACJA (Standard Scaler / IQR)
//      float norm_distance = (distance_f - NORM_RANGING_CENTER) / NORM_RANGING_IQR;
//      float norm_signal   = (signal_f - NORM_SIGNAL_CENTER) / NORM_SIGNAL_IQR;
//
//      // 4. OBRÓT O 180 STOPNI (Kluczowy krok dla modelu CNN!)
//      // Zamieniamy indeks odczytu 'i' na odwrócony indeks zapisu 'rotated_idx'
//      // int rotated_idx = 63 - i;
//
//      // 5. ZAPIS DO BUFORA WEJŚCIOWEGO AI
//      // Sieć przyjmuje 128 wejść (64 strefy * 2 cechy) ułożonych naprzemiennie
//      ai_input_buffer[2 * rotated_idx]     = norm_distance;
//      ai_input_buffer[2 * rotated_idx + 1] = norm_signal;
//  }
//
//  return 0; // Gotowe do inferencji
//}

void acquire_data(HANDPOSTURE_converted_data *Ranging_converted_data, RANGING_SENSOR_Result_t *Data_ToF)
{

    for (int i = 0; i < 64; i++) //tutaj przenosimy odczytane dane do naszej struktury, na ktorej bedziemy pracowac w celu integralnosci danych
    {
   		Ranging_converted_data->ranging[i] = (float)Data_ToF->ZoneResult[i].Distance[0];
        Ranging_converted_data->peak[i] = Data_ToF->ZoneResult[i].Signal[0];
        Ranging_converted_data->targets[i] = Data_ToF->ZoneResult[i].NumberOfTargets;
        Ranging_converted_data->status[i] = Data_ToF->ZoneResult[i].Status[0];
    }
}

void validate_frame(HANDPOSTURE_converted_data *Ranging_converted_data){
	float min = 4000.0;
	for (int i = 0; i < 64; i++){
		if (Ranging_converted_data->targets[i] > 0
				&& Ranging_converted_data->status[i] == 0
				&& Ranging_converted_data->ranging[i] < min){
			min = Ranging_converted_data->ranging[i];  //sprawdzilismy najmniejszy dystans zmierzony w danej klatce
			Ranging_converted_data->min_value = min;
		}
	}

	Ranging_converted_data->min_value = min;

	if (min < 400.0 && min > 100.0){
		Ranging_converted_data->is_valid_frame = 1;
	}
	else {
		Ranging_converted_data->is_valid_frame = 0;
	}
}

void clean_frame(HANDPOSTURE_converted_data *Ranging_converted_data){
	bool valid;
	float background_removal = 120.0;
	float default_ranging_value = 4000.0;
	float default_signal_value = 0.0;

	for (int i = 0; i < 64; i++){
		valid = (Ranging_converted_data->targets[i] > 0)
				&& (Ranging_converted_data->status[i] == 0)
				&& (Ranging_converted_data->ranging[i] < Ranging_converted_data->min_value + background_removal);
		if (!valid){
			Ranging_converted_data->ranging[i] = default_ranging_value;
			Ranging_converted_data->peak[i] = default_signal_value;
		}
	}

}

void normalize_data(HANDPOSTURE_converted_data *Ranging_converted_data, float *normalized_data_ai){
	float normalization_ranging_center = 295.0;
	float normalization_ranging_iqr = 196.0;
	float normalization_signal_center = 281.0;
	float normalization_signal_iqr = 452.0;
	for (int i = 0; i < 64; i++){
		normalized_data_ai[2*i] = (Ranging_converted_data->ranging[i] - normalization_ranging_center / normalization_ranging_iqr);
		normalized_data_ai[2*i+1] = (Ranging_converted_data->peak[i] - normalization_signal_center / normalization_signal_iqr);
	}
}

static int argmax(const float *values, uint32_t len, float threshold)
{
  float max_value = values[0];
  uint32_t max_index = 0;
  for (uint32_t i = 1; i < len; i++)
  {
    if (values[i] > max_value && values[i] > threshold)
    {
      max_value = values[i];
      max_index = i;
    }
  }
  return(max_index);
}

static void label_filter(int current_label, OUTPUT_labels *plabels)
{
  if (current_label == plabels->previous_label)
  {
    if (plabels->label_counter < 3)
    	plabels->label_counter++;
    else if (plabels->label_counter == 3)
    	plabels->handposture_label = current_label;
    else
    	plabels->label_counter = 0;
  }
  else
  {
	  plabels->label_counter = 0;
#if KEEP_LAST_VALID == 0
	  plabels->handposture_label = 0;
#endif
  }

  plabels->previous_label = current_label;
}

void output_selection(OUTPUT_labels *plabels, float *ai_ouput){
	int current_label = 0;
	float threshold = 0.9;
	current_label = argmax(ai_ouput, 8, threshold);
	label_filter(current_label, plabels);
}

int post_process(ai_i8* data[])
{
  /* process the predictions
  for (int idx=0; idx < AI_CNN_2D_EDGING_AI_OUT_NUM; idx++ )
  {
      data[idx] = ....
  }

  */
  return 0;
}

/* USER CODE END 2 */

/* Entry points --------------------------------------------------------------*/

void MX_X_CUBE_AI_Init(void)
{
    /* USER CODE BEGIN 5 */
  printf("\r\nAI INIT\r\n");

  ai_boostrap(data_activations0);
    /* USER CODE END 5 */
}

void MX_X_CUBE_AI_Process(void)
{
    /* USER CODE BEGIN 6 */
	ai_input->format = AI_BUFFER_FORMAT_FLOAT;
	ai_input->data = (ai_handle)ai_data_input;
	ai_input->size = 128;
	ai_input->meta_info = NULL;
	ai_input->flags = 0;

	ai_run();

	memcpy(ai_data_output, (float*)ai_output->data, 8 * sizeof(float));

    /* USER CODE END 6 */
}
#ifdef __cplusplus
}
#endif
