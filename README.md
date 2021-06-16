# RaspberryPI

DGSW-Smart-Farm RasberryPI
*************
### 기능
라즈베리파이 기능 설명
#### arduino serial 통신
  * arduino에서 보내주는 값 받아오기
    * humidity, temprature, soil_humidity, air
  * arduino에 제어 명령 보내기
    * A : led on, a : led off, B : fan on, b : fan off

#### mqtt 프로토콜 사용
  * server로 센서 값 보내기
  * server에서 제어 명령 받기
    * smartfarm/control - led on, led off, fan on, fan off
