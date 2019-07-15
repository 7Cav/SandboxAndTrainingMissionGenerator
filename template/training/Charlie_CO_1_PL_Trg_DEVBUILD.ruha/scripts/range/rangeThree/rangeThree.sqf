hint "Resetting range...";

_targets = [tgt3_1,tgt3_2,tgt3_3,tgt3_4,tgt3_5,tgt3_6,tgt3_7,tgt3_8,tgt3_9,tgt3_10];
{_x  animate["terc",1]} forEach _targets;
sleep 3;
{_x  animate["terc",0]} forEach _targets;
sleep 1;
hint "Range reset...";