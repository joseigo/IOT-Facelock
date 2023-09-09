//Insira seu nome de usuário e chave. Você encontra essas informações acessando
//sua conta no Adafruit IO
#define IO_USERNAME "joseigo"
#define IO_KEY "aio_pnbi48Ofk6lmJhgF1Gh4NJId60xS"

/********************* Configuração do WIFI **************************************/

//Insira o SSID e Senha da rede WIFI a qual você irá conectar
#define WIFI_SSID "brisa-2138502"
#define WIFI_PASS "sapij9f7"


/***************Configurações do comunicaçaão************/
#include "AdafruitIO_WiFi.h"

AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS);

/************************ Mapeamento de IO *******************************/
#define LEDG 18  //pino de saida para acionamento da Led verde
#define LEDR 19   //pino de saida para acionamento da led vermelho


/************************ Configuração dos tópicos *******************************/

// configura o tópico
AdafruitIO_Feed *feedLed = io.feed("lib");


/************************ Função setup *******************************/

void setup() {

  //configura pino dos leds como saída
  pinMode(LEDR,OUTPUT);
  pinMode(LEDG,OUTPUT);

  // configura comunicação serial
  Serial.begin(115200);

  // Aguarda serial monitor
  while(! Serial);

  conectaBroker(); //função para conectar ao broker


}

/************************ Função loop *******************************/

void loop() {

  // processa as mensagens e mantêm a conexão ativa
  byte state = io.run();

  //verifica se está conectado
  if(state == AIO_NET_DISCONNECTED | state == AIO_DISCONNECTED){
    conectaBroker(); //função para conectar ao broker
  }
 
}

/****** Função de tratamento dos dados recebidos em L1***************/

void handleLed(AdafruitIO_Data *data) {

  // Mensagem
  Serial.print("Recebido  <- ");
  Serial.print(data->feedName());
  Serial.print(" : ");
  Serial.println(data->value());

  //Aciona saída conforme dado recebido
  if(data->isTrue()){
    digitalWrite(LEDG, HIGH);
    digitalWrite(LEDR, LOW);
  }
  else{
    digitalWrite(LEDR, HIGH);
    digitalWrite(LEDG, LOW);
  }
}


/****** Função para conectar ao WIFI e Broker***************/

void conectaBroker(){
 
  //mensagem inicial
  Serial.print("Conectando ao Adafruit IO");

  // chama função de conexão io.adafruit.com
  io.connect();

   // instancia um novo handler para recepção da mensagem do feed Rele
  feedLed->onMessage(handleLed);

  // Aguarda conexação ser estabelecida
  while(io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  // Conectado
  Serial.println();
  Serial.println(io.statusText());

  // certifique-se de que todos os feeds obtenham seus valores atuais imediatamente
  feedLed->get();
}