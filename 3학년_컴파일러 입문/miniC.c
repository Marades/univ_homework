#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#pragma warning(disable : 4996)

#define NO_KEYWORDS 7
#define ID_LENGTH 12

char id[ID_LENGTH];

enum tsymbol {
	tnull = -1,
	tnot, tnotequ, tmod, tmodAssign, tident, tnumber,
	tand, tlparen, trparen, tmul, tmulAssign, tplus,
	tinc, taddAssign, tcomma, tminus, tdec, tsubAssign,
	tdiv, tdivAssign, tsemicolon, tless, tlesse, tassign,
	tequal, tgreat, tgreate, tlbracket, trbracket, teof,
	tconst, telse, tif, tint, treturn, tvoid,
	twhile, tlbrace, tor, trbrace
};

struct tokenType {
	int number;
	union {
		char id[ID_LENGTH];
		int num;
	}value;
};

char *keyword[NO_KEYWORDS] = {
	"const", "else", "if", "int", "return", "void", "while"
};

enum tsymbol tnum[NO_KEYWORDS] = {
	tconst, telse, tif, tint, treturn, tvoid, twhile
};

void lexicalError(int n) {
	printf(" ***  Lexical Error : ");
	switch (n) {
	case 1: printf("an identifier length must be less than 12.\n");
		break;
	case 2: printf("next character must be &.\n");
		break;
	case 3: printf("next character must be |.\n");
		break;
	case 4: printf("invalid character!!!\n");
		break;
	}
}

int superLetter(char ch)
{
	if (isalpha(ch) || ch == '_') return 1;
	else return 0;
}

int superLetterOrDigit(char ch)
{
	if (isalnum(ch) || ch == '_') return 1;
	else return 0;
}

int hexValue(char ch)
{
	switch (ch) {
	case '0': case '1': case '2': case '3': case '4':
	case '5': case '6': case '7': case '8': case '9':
		return (ch - '0');
	case 'A': case 'B': case 'C': case 'D': case 'E': case 'F':
		return (ch - 'A' + 10);
	case 'a': case 'b': case 'c': case 'd': case 'e': case 'f':
		return (ch - 'a' + 10);

	default: return -1;
	}
}

int getIntNum(char firstCharacter, FILE* source_file)
{
	int num = 0;
	int value;
	char ch;

	if (firstCharacter != '0') {                        // decimal
		ch = firstCharacter;
		do {
			num = 10 * num + (int)(ch - '0');
			ch = fgetc(source_file);
		} while (isdigit(ch));
	}
	else {
		ch = fgetc(source_file);
		if ((ch >= '0') && (ch <= '7'))                // octal
			do {
				num = 8 * num + (int)(ch - '0');
				ch = fgetc(source_file);
			} while ((ch >= '0') && (ch <= '7'));
		else if ((ch == 'X') || (ch == 'X')) {        // hexa decimal
			while ((value = hexValue(ch = fgetc(source_file))) != -1)
				num = 16 * num + value;
		}
		else num = 0;                                                // zero
	}
	ungetc(ch, stdin);        // retract
	return num;
}

struct tokenType scanner(FILE * src_file) {
	struct tokenType token;
	int i, index;
	char ch, id[ID_LENGTH];

	token.number = tnull;

	do {
		while (isspace(ch = fgetc(src_file)));
		if (superLetter(ch)) {
			i = 0;
			do {
				if (i < ID_LENGTH) id[i++] = ch;
				ch = fgetc(src_file);
			} while (superLetterOrDigit(ch));
			if (i >= ID_LENGTH) lexicalError(1);
			id[i] = '\0';
			ungetc(ch, stdin);

			for (index = 0; index < NO_KEYWORDS; index++)
				if (!strcmp(id, keyword[index]))	break;
			if (index < NO_KEYWORDS)
				token.number = tnum[index];
			else {
				token.number = tident;
				strcpy(token.value.id, id);
			}
		}
		else if (isdigit(ch)) {
			token.number = tnumber;
			token.value.num = getIntNum(ch, src_file);
		}
		else switch (ch) {
		case '/':
			ch = fgetc(src_file);
			if (ch == '*')
				do {
					while (ch != '*') ch = fgetc(src_file);
					ch = fgetc(src_file);
				} while (ch != '/');
			else if (ch == '/')
				while (fgetc(src_file) != '\n');
			else if (ch == '=') token.number = tdivAssign;
			else {
				token.number = tdiv;
				ungetc(ch, stdin);
			}
			break;
		case '!':
			ch = fgetc(src_file);
			if (ch == '=') token.number = tnotequ;
			else {
				token.number = tnot;
				ungetc(ch, stdin);
			}
			break;
		case '%':
			ch = fgetc(src_file);
			if (ch == '=')
				token.number = tmodAssign;
			else {
				token.number = tmod;
				ungetc(ch, stdin);
			}
			break;
		case '&':
			ch = fgetc(src_file);
			if (ch == '&') token.number = tand;
			else {
				lexicalError(2);
				ungetc(ch, stdin);
			}
			break;
		case '*':
			ch = fgetc(src_file);
			if (ch == '=') token.number = tmulAssign;
			else {
				token.number = tmul;
				ungetc(ch, stdin);
			}
			break;
		case '+':
			ch = fgetc(src_file);
			if (ch == '+') token.number = tinc;
			else if (ch == '=') token.number = taddAssign;
			else {
				token.number = tplus;
				ungetc(ch, stdin);
			}
			break;
		case '-':
			ch = fgetc(src_file);
			if (ch == '-') token.number = tdec;
			else if (ch == '=') token.number = tsubAssign;
			else {
				token.number = tminus;
				ungetc(ch, stdin);
			}
			break;
		case '<':
			ch = fgetc(src_file);
			if (ch == '=') token.number = tlesse;
			else {
				token.number = tless;
				ungetc(ch, stdin);
			}
			break;
		case '=':
			ch = fgetc(src_file);
			if (ch == '=') token.number = tequal;
			else {
				token.number = tassign;
				ungetc(ch, stdin);
			}
			break;
		case '>':
			ch = fgetc(src_file);
			if (ch == '=') token.number = tgreate;
			else {
				token.number = tgreat;
				ungetc(ch, stdin);
			}
			break;
		case '|':
			ch = fgetc(src_file);
			if (ch == '|') token.number = tor;
			else {
				lexicalError(3);
				ungetc(ch, stdin);
			}
			break;
		case '(': token.number = tlparen;		break;
		case ')': token.number = trparen;		break;
		case ',': token.number = tcomma;		break;
		case ';': token.number = tsemicolon;	break;
		case '[': token.number = tlbracket;		break;
		case ']': token.number = trbracket;		break;
		case '{': token.number = tlbrace;		break;
		case '}': token.number = trbrace;		break;
		case EOF: token.number = teof;			break;
		default: {
			printf("Current character : %c", ch);
			lexicalError(4);
			break;
		}
		} //switch ent
	} while (token.number == tnull);
	return token;
}

void main() {
	FILE * file;
	int i;
	struct tokenType token;

	if ((file = fopen("perfect.mc", "r")) == NULL) {
		fprintf(stderr, "perfect.mc file not found\n");
		exit(-1);
	}
	
	printf("Scanner Start\n");
	do {
		for (i = 0; i<ID_LENGTH; i++)
			id[i] = ' ';
		token = scanner(file);
		fprintf(stdout, "Token ---> ");

		if (token.number == 5) {
			for (i = 0; i<ID_LENGTH; i++)
				fprintf(stdout, "%c", id[i]);
			fprintf(stdout, ": (%d, %d)\n", token.number, token.value.num);
		}
		else if (token.number == 4) {
			for (i = 0; i<ID_LENGTH; i++)
				fprintf(stdout, "%c", id[i]);
			fprintf(stdout, ": (%d, %s)\n", token.number, token.value.id);
		}
		else {
			for (i = 0; i<ID_LENGTH; i++)
				fprintf(stdout, "%c", id[i]);
			fprintf(stdout, ": (%d, 0)\n", token.number);
		}
	} while (!feof(file));

	fclose(file);
	
}