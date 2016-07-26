from Entities.hexmap import Axial

testAxial = Axial(1, 2)
anotherAxial = Axial(5, -4)

newAxial = testAxial + anotherAxial
print(newAxial.q, newAxial.r)

newAxial *= 3
print(newAxial.q, newAxial.r)
