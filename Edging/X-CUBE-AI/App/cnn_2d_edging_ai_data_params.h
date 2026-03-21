/**
  ******************************************************************************
  * @file    cnn_2d_edging_ai_data_params.h
  * @author  AST Embedded Analytics Research Platform
  * @date    2026-03-19T20:38:52+0100
  * @brief   AI Tool Automatic Code Generator for Embedded NN computing
  ******************************************************************************
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  ******************************************************************************
  */

#ifndef CNN_2D_EDGING_AI_DATA_PARAMS_H
#define CNN_2D_EDGING_AI_DATA_PARAMS_H

#include "ai_platform.h"

/*
#define AI_CNN_2D_EDGING_AI_DATA_WEIGHTS_PARAMS \
  (AI_HANDLE_PTR(&ai_cnn_2d_edging_ai_data_weights_params[1]))
*/

#define AI_CNN_2D_EDGING_AI_DATA_CONFIG               (NULL)


#define AI_CNN_2D_EDGING_AI_DATA_ACTIVATIONS_SIZES \
  { 1096, }
#define AI_CNN_2D_EDGING_AI_DATA_ACTIVATIONS_SIZE     (1096)
#define AI_CNN_2D_EDGING_AI_DATA_ACTIVATIONS_COUNT    (1)
#define AI_CNN_2D_EDGING_AI_DATA_ACTIVATION_1_SIZE    (1096)



#define AI_CNN_2D_EDGING_AI_DATA_WEIGHTS_SIZES \
  { 11008, }
#define AI_CNN_2D_EDGING_AI_DATA_WEIGHTS_SIZE         (11008)
#define AI_CNN_2D_EDGING_AI_DATA_WEIGHTS_COUNT        (1)
#define AI_CNN_2D_EDGING_AI_DATA_WEIGHT_1_SIZE        (11008)



#define AI_CNN_2D_EDGING_AI_DATA_ACTIVATIONS_TABLE_GET() \
  (&g_cnn_2d_edging_ai_activations_table[1])

extern ai_handle g_cnn_2d_edging_ai_activations_table[1 + 2];



#define AI_CNN_2D_EDGING_AI_DATA_WEIGHTS_TABLE_GET() \
  (&g_cnn_2d_edging_ai_weights_table[1])

extern ai_handle g_cnn_2d_edging_ai_weights_table[1 + 2];


#endif    /* CNN_2D_EDGING_AI_DATA_PARAMS_H */
