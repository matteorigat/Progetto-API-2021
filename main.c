#include <stdio.h>
#include <stdlib.h>
#define INFINITO 4294967295
unsigned int *classifica, *costo;

unsigned int sommacammini(unsigned int **grafo, unsigned int d){
    unsigned int visto[d], costi[d], i, nodo = 0, cont = 0, costominimo;

    for(i=1; i<d; i++){
        if((costi[i] = grafo[0][i]) == 0)
            cont++;
        visto[i] = 0;
    }

    if(cont == d-1)
        return 0;

    for(cont=2; cont<d; cont++){

        costominimo = INFINITO;

        for(i=1; i<d; i++)
            if(visto[i] != 1)
               if(costominimo > costi[i] && costi[i] != 0){
                  costominimo = costi[i];
                  nodo = i;
               }

        visto[nodo] = 1;

        for(i=1; i<d; i++)
            if(visto[i] != 1)
               if(grafo[nodo][i] != 0)
                  if(costi[i] > costominimo + grafo[nodo][i] || costi[i] == 0)
                     costi[i] = costominimo + grafo[nodo][i];   
    }

    cont = costi[1];
    for(i=2; i<d; i++)
        cont = cont + costi[i];

    return cont;
}

void swap(unsigned int *a, unsigned int *b){
    unsigned int c;

     c = *a;
    *a = *b;
    *b = c;
}

void max_heapify(unsigned int n, unsigned int k){
    unsigned int left = 2*n, right = 2*n+1, posmax;

    if(left < k && costo[left] > costo[n])
        posmax = left;
    else
        posmax = n;
    
    if(right < k && costo[right] > costo[posmax])
        posmax = right;

    if(posmax != n){
        swap(&costo[n], &costo[posmax]);
        swap(&classifica[n], &classifica[posmax]);
        max_heapify(posmax, k);
    }
}

void costruisci_maxheap(unsigned int k){
    unsigned int n;

    for(n=k/2; n>0; n--)
        max_heapify(n-1, k);    
}

void stampa(unsigned int n){

    if(n/10 != 0)
        stampa(n/10);
    
    putchar_unlocked((n%10) + 48);
}

int main(){
    unsigned int indice=0, d=0, k=0, i, j, somma, **grafo;
    char input, c;

    c = getchar_unlocked();

    while(c > 47 && c < 58){
        d = d * 10 + c - 48;
        c = getchar_unlocked();
    }

    c = getchar_unlocked();

    while(c > 47 && c < 58){
        k = k * 10 + c - 48;
        c = getchar_unlocked();
    }

    classifica=(unsigned int *)malloc(k*sizeof(unsigned int));
    costo=(unsigned int *)malloc(k*sizeof(unsigned int));
    
    grafo=(unsigned int **)malloc(d*sizeof(unsigned int *));
    for(i=0; i<d; i++)
        grafo[i]=(unsigned int *)malloc(d*sizeof(unsigned int));
    
    do{

       if((input = getchar_unlocked()) == EOF)
          return 0;

       while((c = getchar_unlocked()) != 10){}

       if(input == 'A'){

          for(i=0; i<d; i++){
                for(j=0; j<d; j++){
                     somma = 0;

                     while((c = getchar_unlocked()) < 48  || c > 57){}

                     while(c > 47 && c < 58){
                          somma = somma * 10 + c - 48;
                          c = getchar_unlocked();
                      }
                      grafo[i][j] = somma;
                }
            }
 
          somma = sommacammini(grafo, d);

          if(indice < k){
            
              classifica[indice] = indice;
              costo[indice] = somma;

              if(indice == k-1)
                  costruisci_maxheap(k);

          }else if(costo[0] > somma){
                   costo[0] = somma;
                   classifica[0] = indice;
                   max_heapify(0, k);
          }

          indice++;

        }else if(input == 'T'){

           if(indice < k)
             for(i=0; i<indice; i++){
                stampa(classifica[i]);
                if(i < indice-1)
                    putchar_unlocked(' ');
              }

            else
             for(i=0; i<k; i++){
                stampa(classifica[i]);
                if(i < k-1)
                    putchar_unlocked(' ');
              }

            putchar_unlocked('\n');        
        }

    }while(input == 'A' || input == 'T');

    return 0;
}
