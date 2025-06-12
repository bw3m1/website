import turtle as tp

n=2

tp.color('white')
tp.left(180)
tp.forward(50)
tp.left(180)
tp.color('black')
for _ in range(round(365/n)):
  tp.forward(n)
  tp.left(1)