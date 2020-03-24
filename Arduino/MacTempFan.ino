#include "LedControl.h"

#define FAN   0
#define TEMP  1

#define CURRENT_POS   1
#define MAX_POS       0

LedControl lc=LedControl(9,5,6,2);  // DataIn - 9, LOAD - 6, CLK - 5, 2 MAX 7219

char buf[80];
int cnt = 0;
boolean parseDone = false;
boolean ignore = false;
float maxTemp = 0.0;
int maxFan = 0;

void setup() {
  Serial.begin(115200);
  
  lc.shutdown(FAN,false);
  lc.setIntensity(FAN,8);     // Set the brightness to a medium values for module 0
  lc.clearDisplay(FAN);       // and clear the display for module 0

  lc.shutdown(TEMP,false);
  lc.setIntensity(TEMP,8);     // Set the brightness to a medium values for module 1
  lc.clearDisplay(TEMP);       // and clear the display for module 1

}

void setTemp(float temp, int pos)
{
  if ((int)(temp/10) != 0) lc.setDigit(TEMP, pos*4+3, (int)(temp/10), false);
  lc.setDigit(TEMP, pos*4+2, (int)temp%10, true);
  lc.setDigit(TEMP, pos*4+1, (int)(temp*10)%10, false);
  lc.setChar(TEMP, pos*4, 'c', false);
}

void setFanRPM(int rpm, int pos)
{
  if ((rpm/1000) != 0) lc.setDigit(FAN, pos*4+3, (int)(rpm/1000), false);
  if ((rpm/100) != 0)  lc.setDigit(FAN, pos*4+2, (int)((rpm/100)%10), false);
  if ((rpm/10) != 0)  lc.setDigit(FAN, pos*4+1, (int)((rpm/10)%10), false);
  lc.setDigit(FAN, pos*4, rpm%10, false);  

}

void loop()
{
  float temp1, temp2;
  int fan1, fan2;
  char *p;
  char tbuf[4];

  if (parseDone) {
    p = strtok(buf, ",");   // get command
    if (*p == 'T') {   // temperature data
      p = strtok(NULL, ",");
      temp1 = atof(p);

      if (temp1 >= maxTemp) {
        maxTemp = temp1;
      }
      setTemp(temp1, CURRENT_POS);
      setTemp(maxTemp, MAX_POS);
      
    } else if (*p == 'F') {  // fan speed data
      p = strtok(NULL, ",");
      fan1 = atoi(p);

      if (fan1 >= maxFan) {
        maxFan = fan1;
      }
      setFanRPM(fan1, CURRENT_POS);
      setFanRPM(maxFan, MAX_POS);
    }
    parseDone = false;    
  } else while (Serial.available()) {
    char c = Serial.read();
    if (ignore == true) {
      if (c == '\n') {
        ignore = false;
        cnt = 0;
      }   
    } else {
      if (!((c == 'T') || (c == 'F') || isdigit(c) || (c == '.') || (c == ',') || (c == '\n'))) {
        ignore = true;
      }
      buf[cnt++] = c;
      if ((c == '\n') || (cnt == sizeof(buf)-1)) {
        buf[cnt] = '\0';
        cnt = 0;
        parseDone = true;
        ignore = false;
      }
    }
  }
}