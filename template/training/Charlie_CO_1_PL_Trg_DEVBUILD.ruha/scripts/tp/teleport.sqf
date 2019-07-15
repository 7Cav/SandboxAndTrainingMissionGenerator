_dest = (_this select 3) select 0;
_dir = random 359;
player SetPos [(_dest select 0)-4*sin(_dir),(_dest select 1)-4*cos(_dir)];