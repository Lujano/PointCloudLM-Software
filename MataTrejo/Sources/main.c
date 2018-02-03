/* ###################################################################
**     Filename    : main.c
**     Project     : Mata
**     Processor   : MC9S08QE128CLK
**     Version     : Driver 01.12
**     Compiler    : CodeWarrior HCS08 C Compiler
**     Date/Time   : 2018-01-17, 15:01, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.12
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */


/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "AS1.h"
#include "Bit1.h"
#include "TI1.h"
#include "Bit2.h"
#include "AD1.h"
#include "AS2.h"
#include "Cap1.h"
/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"

/* User includes (#include below this line is not maintained by Processor Expert) */

unsigned char estado = ESPERAR;
unsigned char CodError;
unsigned int Enviados = 2;		// Esta variable no aporta nada más sino el número de elementos del arreglo a enviar.
unsigned int error;
bool primero = FALSE;
unsigned int periodo;

unsigned int ADC16;



unsigned char cTrama[5]={0x00,0x00,0x00,0x00,0xFF}; 	// Esta es una primera trama que yo hice de ejemplo.
unsigned char dTrama[2]={0x00,0x00};			// Esta es la trama que declaré para rellenarla con la medición del ADC.	

void main(void)
{
  /* Write your local variable definition here */

	
  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
  PE_low_level_init();
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
    
  /* For example: for(;;) { } */

  for(;;){

  	switch (estado){
  		
  		case ESPERAR:
  			break;
  			
  		case MEDIR:
  			CodError = AD1_Measure(TRUE);
  			CodError = AD1_GetValue16(&ADC16);
  			estado = ENVIAR;
  			break;
  	
  		case ENVIAR:
  			
			/*
			
			if(iADC.u8[0] != 0xFF){
  				cTrama[1] = iADC.u8[0];
  				cTrama[3] = 0x00;	
  			}else{
  				cTrama[1] = 0xFE;
  				cTrama[3] = 0x00;
  			}
  			
  			if(iADC.u8[1] != 0xFF){
  				cTrama[2] = iADC.u8[1];				
  			}else{
  				cTrama[2] = 0xFE;
  				cTrama[3] = cTrama[3] | 0x0A;	//Esta tiene el protocolo completo.
  			}					//Al final yo solo quiero que miren la sintaxis de las funciones.
  	
						
  			dTrama[0]=(periodo >> 8) & (0xFF);
  			dTrama[1]=(periodo) & (0xFF);
			
			*/
			
			// ENVIAR SOLO LA MEDICIÓN DE 16 BITS SIN TRAMA NI PROTOCOLO:
  			AS1_SendChar(0xFF);//Enviar anuncio de data
  			dTrama[1] = (ADC16>>12) & (0xFF);
  			dTrama[0] = (ADC16>>4) & (0xFF);
  			AS2_SendChar(0x02);
  			CodError = AS1_SendBlock(dTrama,2,&Enviados); //El arreglo con la medición está en iADC.u8 (notar que es un apuntador)
  			estado = ESPERAR;
  			
  			break;
  			
  		default:
  			break;
  	
  	}
  }
  
  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END ProcessorExpert */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.3 [05.08]
**     for the Freescale HCS08 series of microcontrollers.
**
** ###################################################################
*/
