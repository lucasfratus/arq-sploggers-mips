operandos = [1, '15(r12)']
reg_end = operandos[1].split('(')[1].split(')')[0]
end = operandos[1].split('(')[0] + reg_end
print(end)