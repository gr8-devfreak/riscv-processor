int main(){

    *(volatile int*)(0x800) = 100;      // 2048th byte = 512th word
    *(volatile int*)(0x804) = 200;      // 2052th byte = 513th word
    *(volatile int*)(0x808) = 300;      // 2056th byte = 514th word
    *(volatile int*)(0x80C) = 400;      // 2060th byte = 515th word
    *(volatile int*)(0x810) = *(int*)(0x800) + *(int*)(0x804) + *(int*)(0x808) + *(int*)(0x80C);    // 2064th byte = 516th word

    // Comparison
    if (*(volatile int*)(0x800)>500){   // 100>500 : False
        *(volatile int*)(0x814) = 1;    // 2068th byte = 517th word
    }
    else{
        *(volatile int*)(0x814) = 2;    // 2068th byte = 517th word
    }

    // Counter
    for (int i=0 ; i<10 ; i++){
        *(volatile int*)(0x818) = i;    // 2072th byte = 518th word
    }

    return 0;
}
