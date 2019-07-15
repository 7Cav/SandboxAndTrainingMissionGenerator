_tpObjects = [
	[tp_Base, "<t color='#00ff00'>   Base</t>"],
	[tp_mission1, "<t color='#00ff00'>   Mission #1</t>"]
	//[tp_maneuver, "Maneuver Course"]
];

{
	_activeObject = _x select 0;
	{
		_dest = _x select 0;
		if(_activeObject != _dest) then {
			_destName = _x select 1;
			_activeObject addAction [_destName, "scripts\tp\teleport.sqf", [getPos _dest]];
		};
	} foreach _tpObjects;
} foreach _tpObjects;