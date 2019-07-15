["Preparing range...","hint"] call BIS_fnc_MP;

_targetsAll = [tgt1_1,tgt1_2,tgt1_3,tgt1_4,tgt1_5,tgt1_6,tgt1_7,tgt1_8,tgt1_9,tgt1_10,tgt1_11,tgt1_12,tgt1_13,tgt1_14,tgt1_15,tgt1_16,tgt1_17,tgt1_18];
_targetSet1 = [tgt1_1,tgt1_2];
_targetSet2 = [tgt1_3,tgt1_4];
_targetSet3 = [tgt1_5,tgt1_6,tgt1_7];
_targetSet4 = [tgt1_8];
_targetSet5 = [tgt1_9];
_targetSet6 = [tgt1_10,tgt1_11,tgt1_12];
_targetSet7 = [tgt1_13,tgt1_14,tgt1_15];
_targetSet8 = [tgt1_16,tgt1_17];
_targetSet9 = [tgt1_18];

{_x  animate["terc",1]} forEach _targetsAll;
sleep 5;
["Range is hot","hint"] call BIS_fnc_MP;
sleep 3;

Hint "set #1"; 
{_x  animate["terc",0]} forEach _targetSet1;
{_x  animate["terc",0]} forEach _targetSet7;
sleep 15;
{_x  animate["terc",1]} forEach _targetSet1;
{_x  animate["terc",1]} forEach _targetSet7;
sleep 5;

Hint "set #2";
{_x  animate["terc",0]} forEach _targetSet2;
{_x  animate["terc",0]} forEach _targetSet6;
sleep 15;
{_x  animate["terc",1]} forEach _targetSet2;
{_x  animate["terc",1]} forEach _targetSet6;
sleep 5;

Hint "set #3";
{_x  animate["terc",0]} forEach _targetSet8;
{_x  animate["terc",0]} forEach _targetSet9;
sleep 25;
{_x  animate["terc",1]} forEach _targetSet8;
{_x  animate["terc",1]} forEach _targetSet9;
sleep 5;

Hint "set #4";
{_x  animate["terc",0]} forEach _targetSet2;
{_x  animate["terc",0]} forEach _targetSet4;
sleep 25;
{_x  animate["terc",1]} forEach _targetSet2;
{_x  animate["terc",1]} forEach _targetSet4;
sleep 5;

Hint "set #5";
{_x  animate["terc",0]} forEach _targetSet1;
{_x  animate["terc",0]} forEach _targetSet7;
sleep 25;
{_x  animate["terc",1]} forEach _targetSet1;
{_x  animate["terc",1]} forEach _targetSet7;
sleep 5;

Hint "set #6";
{_x  animate["terc",0]} forEach _targetSet3;
{_x  animate["terc",0]} forEach _targetSet6;
sleep 15;
{_x  animate["terc",1]} forEach _targetSet3;
{_x  animate["terc",1]} forEach _targetSet6;
sleep 5;

Hint "set #7";
{_x  animate["terc",0]} forEach _targetSet5;
{_x  animate["terc",0]} forEach _targetSet8;
sleep 25;
{_x  animate["terc",1]} forEach _targetSet5;
{_x  animate["terc",1]} forEach _targetSet8;
sleep 5;

Hint "set #8";
{_x  animate["terc",0]} forEach _targetSet2;
{_x  animate["terc",0]} forEach _targetSet4;
sleep 25;
{_x  animate["terc",1]} forEach _targetSet2;
{_x  animate["terc",1]} forEach _targetSet4;
sleep 5;

Hint "set #9";
{_x  animate["terc",0]} forEach _targetSet7;
{_x  animate["terc",0]} forEach _targetSet8;
sleep 15;
{_x  animate["terc",1]} forEach _targetSet7;
{_x  animate["terc",1]} forEach _targetSet8;
sleep 5;

Hint "set #10";
{_x  animate["terc",0]} forEach _targetSet1;
{_x  animate["terc",0]} forEach _targetSet2;
sleep 15;
{_x  animate["terc",1]} forEach _targetSet1;
{_x  animate["terc",1]} forEach _targetSet2;
sleep 5;


["End of course","hint"] call BIS_fnc_MP;

{_x  animate["terc",0]} forEach _targetsAll;
rangeOne = 0;