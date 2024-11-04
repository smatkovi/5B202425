turn=1
aa=0
ab=0
ac=0
ba=0
bb=0
bc=0
ca=0
cb=0
cc=0
run=True
vacant=True
draw=0
while run==True:
  while vacant:
    entered = input("Koordinaten eingeben")
    if globals()[entered] == 0:
      if turn == 1:
        globals()[entered] = 1
      else:
        globals()[entered] = 4
      vacant = False
    else:
      print("Feld ist schon besetzt")
  turn *= (-1)
  print(aa,"|",ab,"|",ac)
  print(ba,"|",bb,"|",bc)
  print(ca,"|",cb,"|",cc)
  if aa+ab+ac == 3:
    print("Person 1 hat gewonnen")
    run = False
  if aa+ab+ac == 12:
    print("Person 2 hat gewonnen")
    run = False
  vacant = True
  draw += 1
  if draw == 9:
    print("unentschieden")
    run = False
