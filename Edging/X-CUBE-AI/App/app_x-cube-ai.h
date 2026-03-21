
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __APP_AI_H
#define __APP_AI_H
#ifdef __cplusplus
extern "C" {
#endif
/**
  ******************************************************************************
  * @file    app_x-cube-ai.h
  * @author  X-CUBE-AI C code generator
  * @brief   AI entry function definitions
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
/* Includes ------------------------------------------------------------------*/
#include "ai_platform.h"

void MX_X_CUBE_AI_Init(void);
void MX_X_CUBE_AI_Process(void);
/* USER CODE BEGIN includes */
#include "53l8a1_ranging_sensor.h"
typedef struct{
	float ranging[64];
	float peak[64];
	uint8_t targets[64];
	uint32_t status[64];
	bool is_valid_frame;
	float min_value;
} HANDPOSTURE_converted_data;

typedef struct{
	uint8_t label_counter;
	uint8_t handposture_label;
	uint8_t previous_label;
} OUTPUT_labels;

void acquire_data(HANDPOSTURE_converted_data *Ranging_converted_data, RANGING_SENSOR_Result_t *Data_ToF);
void validate_frame(HANDPOSTURE_converted_data *Ranging_converted_data);
void clean_frame(HANDPOSTURE_converted_data *Ranging_converted_data);
void normalize_data(HANDPOSTURE_converted_data *Ranging_converted_data, float *normalized_data_ai);
static int argmax(const float *values, uint32_t len, float threshold);
void output_selection(OUTPUT_labels *plabels, float *ai_ouput);
static void label_filter(int current_label, OUTPUT_labels *plabels);
/* USER CODE END includes */
#ifdef __cplusplus
}
#endif
#endif /*__STMicroelectronics_X-CUBE-AI_10_2_0_H */
