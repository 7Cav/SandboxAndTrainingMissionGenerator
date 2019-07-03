_dest = _this select 3;
_dir = random 359;
_unit = _this select 1;
//_veh = vehicle _unit;
//_unit SetPos [(getMarkerPos _dest select 0)-5*sin(_dir),(getMarkerPos _dest select 1)-5*cos(_dir)];
//_veh SetPos [(getPos _dest select 0)-5*sin(_dir),(getPos _dest select 1)-5*cos(_dir)];
_unit SetPos [(getPos _dest select 0)-5*sin(_dir),(getPos _dest select 1)-5*cos(_dir)];