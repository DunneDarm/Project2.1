/*
 * Temperatuursensor.c
 *
 * Created: 30-Oct-19 7:22:51 PM
 * Author : Casper Scholte-Albers & Sybren Kuiper
 *
 */ 

#include <avr/io.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include<util/delay.h>
#include <avr/interrupt.h>

#define LED1 0
#define LED2 1
#define LED3 2

int ADCRead;
char String[20];
float Rolluik;

//Values that determine the state, max and min high of the screen.
int gv_status;
int current_uitrol;
int min_uitrol;
int max_uitrol;

//Values the determine the state, max temp and min temp settings for the screens/leds.
double current_temp;
int temp_grens_MAX = 23;
int temp_grens_MIN = 5;

//######################################################################################
//The veriables are required for the ultrasonor sensor
volatile uint32_t gv_counter; // 16 bit counter value
volatile uint8_t gv_echo; // a flag
float centi = 0; //global variable for distance
volatile uint8_t rising;

int DistanceString[20];
int DistanceRead;

// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51

void uart_init()
{
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter and enable receiver
	UCSR0B=_BV(TXEN0) | _BV(RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C=_BV(UCSZ01)|_BV(UCSZ00);
}

void uart_send(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A,UDRE0);
	// send the data
	UDR0=data;
}

void USART_putstring(char* StringPtr){
	
	while(*StringPtr != 0x00){
		uart_send(*StringPtr);
		StringPtr++;
	}
}

uint8_t uart_getchar(void) {
//Non blocking, checks for input. if there is none then it skips this part.
	if(bit_is_set(UCSR0A, RXC0)){
		return UDR0;
	}
}

//#####################################################################################################################
//Code below is used for the temperature sensor.

void AVRRealSetup(){
	//This sets the channel that the ADC will look at.
	//ADMUX = 1
	
	//Sets the prescaler to 128. (Atmega328p Datascheet page 264)
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));
	 
	//Sets the voltage reference to 5V
	ADMUX |= (1<<REFS0);
	ADMUX &= ~(1<<REFS1);
	
	//ADC in free-running mode
	ADCSRB &= ~((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));  
	  
	//Signal source, in this case is the free-running
	ADCSRA |= (1<<ADATE);               
	
	//ADC enable bit, this turns the ADC on
	ADCSRA |= (1<<ADEN);
	
	//ADC start conversion bit set to 1.
	ADCSRA |= (1<<ADSC);
}

void TempCalc(){
	//Analog gives back a value of 10 bits (0-1023). this is Stored in ADCW
	double temp;
	temp = ADCW * 5;
	temp = temp / 1024;
	temp = temp - 0.5;
	temp = temp * 100;
	ADCRead = temp;
	current_temp = ADCRead;
}

//Code below is used for the screen/lights
void DetermineGoal(uint8_t goal){
	if(goal == 0){
		gv_status = 0;
	}
	if(goal == 1){
		gv_status = 1;
	}
}


//Led system for solarpannel
void Rol_uit_in(){
	if (gv_status == 0)//Als het rolluik is opgerold | Green light
	{
		while (current_uitrol < max_uitrol)
		{
			PORTB |= (1 << LED1);
			PORTB |= (1 << LED3);
			_delay_ms(100);
			current_uitrol += 10;
			PORTB &=~ (1 << LED3);
			_delay_ms(100);
		}
		PORTB &=~ (1 << LED1);
	}
	if (gv_status == 1)//Als het rolluik is  | Red Light
	{
		while (current_uitrol > min_uitrol)
		{
			PORTB |= (1 << LED2);
			PORTB |= (1 << LED3);
			_delay_ms(100);
			current_uitrol -= 10;
			PORTB &=~ (1 << LED3);
			_delay_ms(100);
		}
		PORTB &=~ (1 << LED2);
	}
}

void check_temp()
{
	if(current_temp >= temp_grens_MAX)
	{
		gv_status = 0;
		Rol_uit_in();
	}
	if (current_temp <= temp_grens_MIN)
	{
		gv_status = 0;
		Rol_uit_in();
	}
	if(current_temp > temp_grens_MIN && current_temp < temp_grens_MAX)
	{
		gv_status = 1;
		Rol_uit_in();
	}
}


void init_ext_int(void)
	{
		// any change triggers ext interrupt 1
		EICRA = (1 << ISC10);
		EIMSK = (1 << INT1);
	}

void init_timer(void)
	{
		TCCR1A = 0;
		TCCR1B = 0;
	}

void Send_signal()
	{
		PORTD |= (1 << PIND4); //Turn on the pull-up, rising edge
		_delay_us(12); //delay enough for the trigger to receive and comprehend
		PORTD = 0;
		gv_echo = 1;
	}

ISR (INT1_vect)
	{
		if (gv_echo == 1)
		{
			TCCR1B |= (1<<CS10) | (0<<CS11) | (1<<CS12);
			TCNT1 = 0;
			//TIMSK0 |= (1<<TOIE0);
			gv_counter = 0;
			gv_echo = 0;
		}
		else{
			TCCR1B = 0;
			centi = TCNT1;
		}
	}

int main(void)
{
	AVRRealSetup();
	uart_init();
	DDRB = 0xFF;
	gv_status = 5;
	current_uitrol = 10;
	min_uitrol = 10;
	max_uitrol = 160;

	init_ext_int();
	init_timer();
	DDRD = 0x16;
	PORTD = 0;
	sei(); //turn on interrupts

	while (1)
	{
		TempCalc();
		//itoa() turns a int into a string.
		//itoa(Int that you want to convert, destination that you want to write the string into, determines what kind of number the result has to be) 10 = decimal, 16 = Hexadecimal, 2 = binary
		itoa(ADCRead, String , 10);

		//Checks for input(Non-blocking) We were not able to finish this on time. Thats why it is set a comments
		//char received_data = uart_getchar();
		//if(received_data == 0){
			//gv_status = 0;
		//}
		//if(received_data == 1){
			//gv_status = 1;
		//}
		
		
		//if data received, determine goal and do somthing based on that.
		//DetermineGoal(received_data);

		check_temp();

        //Code used for sending temperature data to python.
		USART_putstring(String);
		USART_putstring("t");
		_delay_ms(100);
		
		
		//Code used for sending the distance sensor data.
		//Send_signal();
		//_delay_ms(30);
		//DistanceRead = ((uint32_t)(centi*1024/16)/58);
		//itoa(DistanceRead, DistanceString, 10);
		//_delay_ms(500);
		//USART_putstring(DistanceString);
		//USART_putstring(" ");
		
	}
}