/*
 * Lichtsensor_project.c
 *
 * Created: 31-10-2019 11:37:21
 *  Author: aline
 */
#include <avr/io.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <avr/sfr_defs.h>
#include <util/delay.h>
#include <stdlib.h>
#include <avr/interrupt.h>

#define F_CPU 16000000 //16E6
#define UBBRVAL 51

int adc_value;

//-----------------------------------------------------------
//lightsensor code
//-----------------------------------------------------------
void ADC_setup(void) {
	//Prescaler at 128 so we have an 125Khz clock source
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));

	//Avcc(+5v) as voltage reference
	ADMUX |= (1<<REFS0);
	ADMUX &= ~(1<<REFS1);

	//ADC in free-running mode
	ADCSRB &= ~((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));

	//Signal source, in this case is the free-running
	ADCSRA |= (1<<ADATE);
	//Power up the ADC
	ADCSRA |= (1<<ADEN);
	//Start converting
	ADCSRA |= (1<<ADSC);
}


void uart_init() {
	// set the baud rate to 19200
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter and enable receiver
	UCSR0B=_BV(TXEN0) | _BV(RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C=_BV(UCSZ01)|_BV(UCSZ00);
}

void uart_send(uint8_t data) {
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A,UDRE0);
	// send the data
	UDR0=data;
}

uint8_t uart_getchar(void) {
	loop_until_bit_is_set(UCSR0A, RXC0); /* Wait until data exists. */
	return UDR0;
}

void USART_putstring(char* StringPtr){
	while(*StringPtr != 0x00) {
		uart_send(*StringPtr);
		StringPtr++;
	}
}


//-----------------------------------------------------------
//led lights code
//-----------------------------------------------------------
#define LED1 0
#define LED2 1
#define LED3 2

volatile uint8_t gv_status;
int current_uitrol;
int min_uitrol;
int max_uitrol;

int licht_grens_MAX = 2300;
int licht_grens_MIN = 800;

void Rol_uit_in() {
	if (gv_status == 0) { //Als het rolluik is opgerold
		while (current_uitrol < max_uitrol) {
			PORTB |= (1 << LED2);
			PORTB |= (1 << LED3);
			_delay_ms(100);
			current_uitrol += 10;
			PORTB &=~ (1 << LED3);
			_delay_ms(100);
		}
		PORTB &=~ (1 << LED2);
	}
	if (gv_status == 1) { //Als het rolluik is uitgerold
		while (current_uitrol > min_uitrol) {
			PORTB |= (1 << LED1);
			PORTB |= (1 << LED3);
			_delay_ms(100);
			current_uitrol -= 10;
			PORTB &=~ (1 << LED3);
			_delay_ms(100);
		}
		PORTB &=~ (1 << LED1);
	}
}

void check_licht() {
	if (adc_value >= licht_grens_MAX) {
		gv_status = 0;
		Rol_uit_in();
	}
	if (adc_value <= licht_grens_MIN) {
		gv_status = 0;
		Rol_uit_in();
	}
	if(adc_value > licht_grens_MIN && adc_value < licht_grens_MAX) {
		gv_status = 1;
		Rol_uit_in();
	}
}

//-----------------------------------------------------------
//distance sensor code
//-----------------------------------------------------------
volatile uint32_t gv_counter; // 16 bit counter value
volatile uint8_t gv_echo; // a flag
float centi = 0; //global variable for distance
volatile uint8_t rising;

int DistanceString[20];
int DistanceRead;

void init_ext_int(void) {
	// any change triggers ext interrupt 1
	EICRA = (1 << ISC10);
	EIMSK = (1 << INT1);
}

void init_timer(void) {
	TCCR1A = 0;
	TCCR1B = 0;
}

void Send_signal() {
	PORTD |= (1 << PIND4); //Turn on the pull-up, rising edge
	_delay_us(12); //delay enough for the trigger to receive and comprehend
	PORTD = 0;
	gv_echo = 1;
}

ISR (INT1_vect) {
	if (gv_echo == 1) {
		TCCR1B |= (1<<CS10) | (0<<CS11) | (1<<CS12);
		TCNT1 = 0;
		gv_counter = 0;
		gv_echo = 0;
	}
	else{
		TCCR1B = 0;
		centi = TCNT1;
	}
}

//------------------------------
//main
//------------------------------
int main(void) {
	ADC_setup();
	char String[20];
	uart_init();

	DDRB = 0xff;
	current_uitrol = 80;
	max_uitrol = 160;
	min_uitrol = 10;
	gv_status = 0;

	init_ext_int();
	init_timer();
	DDRD = 0x16;
	PORTD = 0;

	sei(); //turn on interrupts

	while(1){        //The infinite loop could also be while(1
		adc_value = ADCW * 8.5;    //Read the ADC value

		itoa(adc_value, String , 10);
		_delay_ms(50);

		check_licht();

		USART_putstring(String);
		USART_putstring("L");

		//enable for the distance sensor
		//Send_signal();
		//_delay_ms(30);
		//DistanceRead = ((uint32_t)(centi*1024/16)/58);
		//itoa(DistanceRead, DistanceString, 10);
		//_delay_ms(500);
		//USART_putstring(DistanceString);
		//USART_putstring(" ");
	}
}