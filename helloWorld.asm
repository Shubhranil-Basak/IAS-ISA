3 //N
0 //j-loop controller
0 //resx
0 //resy
0 //resx^2
0 //resy^2
0 //magnitude of resultant
0 //decimal part of value of resultant
10 //temp-to store memory location of the starting of the vector
1 //x0
2 //x1
3 //x2
0 //x3
0 //x4
0 //buffer space for extra x components
0
0
0
0
2 //y0
3 //y1
4 //y2
0 //y3
0 //y4
0 //buffer space for extra y components
0
1
0
0
10 //a variable which stores 10
LOAD M(1) ; SUB M(27) //
STOR M(2) ; LOAD M(2) // j=N-1
LOAD M(2) ; JUMP+ M(35,0:19) //if N==0 => j==-1 so next instruction halt is executed and program terminates
HALT ; NOP //
LOAD M(3) ; ADD M(10) //
STOR M(3) ; LOAD M(4) //resx = resx+xi
LOAD M(4) ; ADD M(20) //
STOR M(4) ; LOAD M(1) //res y= resy+yi
LOAD M(1) ; SUB M(2) //AC=N-j
ADD M(9) ; STOR M(35,28:39) // AC=AC+temp, changing the address to the next xi
ADD M(30) ; STOR M(37,28:39) // AC=AC+2*N, changing the address to the next yi
NOP ; LOAD M(2)
LOAD M(2) ; SUB M(27) //
STOR M(2) ; LOAD M(2) //j=j-1
JUMP+ M(33,0:19) ; LOAD M(3) //while(j>=0)
LOAD M(3) ; MUL M(3)
LOAD MQ ; STOR M(5) //resx^2=resx**2
LOAD M(4) ; MUL M(4)
LOAD MQ ; STOR M(6) //resy^2=resy**2
LOAD M(5) ; ADD M(6) //AC=resx^2+resy^2
NOP ; STOR M(7) //computing square root of value stored in AC, storing int part in AC and dec part in MQ, int_val_of_mag_of_res=AC
LOAD MQ ; STOR M(8) //dec_val_of_mag_of_res=MQ
HALT ; NOP //