
_targetsAll = [tgt2_1,tgt2_2,tgt2_3,tgt2_4,tgt2_5,tgt2_6,tgt2_7,tgt2_8,tgt2_9,tgt2_10,tgt2_11,tgt2_12,tgt2_13,tgt2_14,tgt2_15,tgt2_16];
_targetsBfar = [tgt2_9,tgt2_10,tgt2_11,tgt2_12];

{_x  animate["terc",1]} forEach _targetsAll;
sleep 2;
{_x  animate["terc",0]} forEach _targetsBfar;