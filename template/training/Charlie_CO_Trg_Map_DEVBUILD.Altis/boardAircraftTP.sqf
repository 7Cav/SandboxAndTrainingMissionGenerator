/*
 * Author: =7Cav=WO1.Raynor.D
 * Adds pilot/crew teleporters from a set of flags to corresponding aircraft. 
 * It will search for flagpoles following the naming scheme <prefix>_flag_<index>.
 * For every flagpole, it will add two actions for moveInCargo and moveInDriver.
 * It will search for the same-index vehicle (at action runtime) following the naming scheme <prefix>_<index>.
 * The script will save the action IDs with the object and remove the old actions if it is re-run with the same prefix.
 *
 * Arguments:
 * 0: Optional - Prefix for variable names <STRING> (default: "c130")
 * 1: Optional - Custom prefix to use in the action text, instead of uppercase variable name. <STRING> (default: "")
 * 2: Optional - Radius of action. Values <= about 3 drop to 0 for some reason. <SCALAR> (default: 3.5)
 * 3: Optional - If you somehow have more than 20 spawners in one group, sets max count to look for. <INTEGER> (default: 20)
 *
 * Return Value:
 * None
 *
 * Example:
 * [] execVM "boardAircraftTP.sqf"; 
 *     default is aircraft named c130_3 and flags named c130_flag_#
 *
 * ["uh60"] execVM "boardAircraftTP.sqf"; 
 *     Naming scheme uh60_# and uh60_flag_#
 * 
 * ["c130", "C-130 #"] execVM "boardAircraftTP.sqf"; 
 *     Default naming scheme, except actions would read "Get in C-130 #1", "Get in C-130 #2", etc.
 */

params [
	['_craftPrefix','c130',[""]],
	["_actionText","",[""]],
	['_distance',3.5,[0]],
	['_maxCount',20,[0]]
];
_found = [];
for '_i' from 1 to _maxCount do {
	_flag = missionNamespace getVariable [format ['%1_flag_%2', _craftPrefix, _i], objNull];
	if(!(isNull _flag)) then {
		removeAllActions _flag;
		_prevIds = _flag getVariable [format ['7Cav_boardTP_actionIDs_%1',_craftPrefix],[]];
		if(count _prevIds > 0) then {
			{_flag removeAction _x} foreach (_flag getVariable ["7Cav_boardTP_actionIDs",[]]);
		};
		_found pushBack _flag;
		diag_log format ['7Cav boardAircraftTP.sqf: Flag: %1_flag_%2 - %3', _craftPrefix, _i, _flag];
		_craftStr = format ['%1_%2', _craftPrefix, _i];
		diag_log format ['7Cav boardAircraftTP.sqf: CraftStr: %1', _craftStr];
		_actionPrefix = if(_actionText == "") then {format ["%1-",toUpper _craftPrefix]} else {_actionText};
		_id1 = _flag addAction [
			format ["<t color='#FFE957'>Get in %1%2</t>", _actionPrefix, _i],
			{(_this select 1) moveInCargo (missionNamespace getVariable [_this select 3, objNull])},
			_craftStr,
			1.5,true,true,"","true",
			_distance
		];
		_id2 = _flag addAction [
			format ["<t color='#FFE957'>Pilot %1%2</t>", _actionPrefix, _i],
			{(_this select 1) moveInDriver (missionNamespace getVariable [_this select 3, objNull])},
			_craftStr,
			1.5,true,true,"","true",
			_distance
		];
		_flag setVariable [format ['7Cav_boardTP_actionIDs_%1',_craftPrefix],[_id1,_id2],true];
	};
};
diag_log format ['7Cav boardAircraftTP.sqf: Flags found: %1', _found];