if(!isServer) exitWith {};
_targetsAll = [tgt1_1,tgt1_2,tgt1_3,tgt1_4,tgt1_5,tgt1_6,tgt1_7,tgt1_8,tgt1_9,tgt1_10,tgt1_11,tgt1_12,tgt1_13,tgt1_14,tgt1_15,tgt1_16,tgt1_17,tgt1_18];

sleep 1;
		if (rangeOne != 1) then {
			rangeOne = 1;
			publicVariable "rangeOne";
			rangeOne_handle = [_this] execVM "scripts\range\rangeOne\rangeOne.sqf";
		} else {
			terminate rangeOne_handle;
			rangeOne = 0;
			publicVariable "rangeOne";
			{_x  animate["terc",0]} forEach _targetsAll;
			["Cease Fire! Cease Fire! Cease Fire!","hint"] call BIS_fnc_MP;
};