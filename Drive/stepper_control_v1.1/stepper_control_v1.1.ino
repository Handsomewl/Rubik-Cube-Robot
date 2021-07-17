#include <Stepper.h>

const int stepsPerRevolution = 200;  // 电机步距角为1.8°，步数为360/1.8=200
const int motorSpeed=120;  //  电机转速为120rpm
//使能控制
const int EN_1=2;
const int EN_2=3;
const int EN_3=4;
const int EN_4=5;
const int EN_5=6;
const int EN_6=7;

char serialMsg[60]={0}; //  储存命令的数组
int cmdLength=0;  //  命令的长度

Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);  //  8，9，10，11管脚为通讯管脚

int stepCount = 0;         // 步数统计

bool isValidMsg(char motor,char command)
{
  if(motor=='U'||motor=='D'||
     motor=='L'||motor=='R'||
     motor=='F'||motor=='B')
     if(command=='1'||command=='2'||command=='3')
      return true;
  return false;
}

void readCmd(int startByte){
  //  读取命令
  char motor=serialMsg[startByte];
  char command=serialMsg[startByte+1];
  int selection=0;
  int operation=0;
  //  判断有效
  if(!isValidMsg(motor,command))
    return;
  //  确定操作 
  switch(motor){
    case 'U':selection=EN_1;break;
    case 'D':selection=EN_2;break;
    case 'L':selection=EN_3;break;
    case 'R':selection=EN_4;break;
    case 'F':selection=EN_5;break;
    case 'B':selection=EN_6;break;
    default: break;
  }
  
  switch(command){
    case '1': operation=-52;break; //  魔方顺时针转90°
    case '2': operation=+52;break;  //  魔方逆时针转90°
    case '3': operation=104;break;  //  转180°
    default:  break;
  }
  //  输出操作
    digitalWrite(selection,HIGH); //  更改使能状态
    myStepper.step(operation);
    digitalWrite(selection,LOW);  //  复位使能状态
  //  返回提示
    stepCount++;
    Serial.print("steps:");
    Serial.print(stepCount);
    Serial.print(" ");
    Serial.print(motor);
    Serial.println(command);
}


void setup() {
  Serial.begin(9600);
  while(Serial.read()>=0){} //  清空串口缓冲区
  myStepper.setSpeed(motorSpeed); //  设置转速
  //  初始化使能状态
  pinMode(EN_1,OUTPUT);
  pinMode(EN_2,OUTPUT);
  pinMode(EN_3,OUTPUT);
  pinMode(EN_4,OUTPUT);
  pinMode(EN_5,OUTPUT);
  pinMode(EN_6,OUTPUT);
  digitalWrite(EN_1,LOW);
  digitalWrite(EN_2,LOW);
  digitalWrite(EN_3,LOW);
  digitalWrite(EN_4,LOW);
  digitalWrite(EN_5,LOW);
  digitalWrite(EN_6,LOW);
}

void loop() {
  while(Serial.available()<=0) //  等待串口接收数据
    delay(10);
  cmdLength=Serial.readBytesUntil('#',serialMsg,60);  //  读命令至数组,并储存命令长度,命令以#结束
  //  判断命令长度是否有效
  if(!cmdLength)
    return;
  if(cmdLength%2) 
    return;

  //  若命令长度有效
  for(int i=0;i<cmdLength;i+=2){
    readCmd(i);
  }
  delay(100);
}
