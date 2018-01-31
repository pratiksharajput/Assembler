%macro  myadd 2
	mov esi,%1
%%pqr:	mov edi,%2
	add esi,edi
	mov eax,esi
	mysub esi,edi
	jmp %%pqr
	%endmacro

%macro  mysub 2
	mov esi,%1
%%xyz:	mov edi,%2
	sub esi,edi		
	mov eax,esi
	mymul esi
	jmp %%xyz
	%endmacro

%macro  mymul 1
	mov esi,%1
	mov eax,esi
	mov ecx,1
%%abc:  
	mov eax,esi
	xor edx,edx
	mul ecx
	pusha
	push eax
	push msg
	call printf
	add esp,8
	popa
	inc ecx
	xor eax,eax
	cmp ecx,10
	jle %%abc
	mymul 5
%endmacro
section .data
	num1 dd 5
	num2 dd 3

section .text
	global main
	extern printf

main:
	mov eax,dword[num1]
	mov ebx,dword[num2]
	mymul eax

