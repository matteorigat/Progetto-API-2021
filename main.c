#include <stdio.h>
#include <stdlib.h>
#define INFINITE 4294967295
unsigned int *rank, *cost;

unsigned int pathsSum(unsigned int **graph, unsigned int d){
    unsigned int visited[d], costs[d], i, node = 0, count = 0, mincost;

    for(i=1; i<d; i++){
        if((costs[i] = graph[0][i]) == 0)
            count++;
        visited[i] = 0;
    }

    if(count == d-1)
        return 0;

    for(count=2; count<d; count++){

        mincost = INFINITE;

        for(i=1; i<d; i++)
            if(visited[i] != 1)
               if(mincost > costs[i] && costs[i] != 0){
                  mincost = costs[i];
                  node = i;
               }

        visited[node] = 1;

        for(i=1; i<d; i++)
            if(visited[i] != 1)
               if(graph[node][i] != 0)
                  if(costs[i] > mincost + graph[node][i] || costs[i] == 0)
                     costs[i] = mincost + graph[node][i];   
    }

    count = costs[1];
    for(i=2; i<d; i++)
        count = count + costs[i];

    return count;
}

void swap(unsigned int *a, unsigned int *b){
    unsigned int c;

     c = *a;
    *a = *b;
    *b = c;
}

void max_heapify(unsigned int n, unsigned int k){
    unsigned int left = 2*n, right = 2*n+1, posmax;

    if(left < k && cost[left] > cost[n])
        posmax = left;
    else
        posmax = n;
    
    if(right < k && cost[right] > cost[posmax])
        posmax = right;

    if(posmax != n){
        swap(&cost[n], &cost[posmax]);
        swap(&rank[n], &rank[posmax]);
        max_heapify(posmax, k);
    }
}

void create_maxheap(unsigned int k){
    unsigned int n;

    for(n=k/2; n>0; n--)
        max_heapify(n-1, k);    
}

void print(unsigned int n){

    if(n/10 != 0)
        print(n/10);
    
    putchar_unlocked((n%10) + 48);
}

int main(){
    unsigned int index=0, d=0, k=0, i, j, sum, **graph;
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

    rank=(unsigned int *)malloc(k*sizeof(unsigned int));
    cost=(unsigned int *)malloc(k*sizeof(unsigned int));
    
    graph=(unsigned int **)malloc(d*sizeof(unsigned int *));
    for(i=0; i<d; i++)
        graph[i]=(unsigned int *)malloc(d*sizeof(unsigned int));
    
    do{

       if((input = getchar_unlocked()) == EOF)
          return 0;

       while((c = getchar_unlocked()) != 10){}

       if(input == 'A'){

          for(i=0; i<d; i++){
                for(j=0; j<d; j++){
                     sum = 0;

                     while((c = getchar_unlocked()) < 48  || c > 57){}

                     while(c > 47 && c < 58){
                          sum = sum * 10 + c - 48;
                          c = getchar_unlocked();
                      }
                      graph[i][j] = sum;
                }
            }
 
          sum = pathsSum(graph, d);

          if(index < k){
            
              rank[index] = index;
              cost[index] = sum;

              if(index == k-1)
                  create_maxheap(k);

          }else if(cost[0] > sum){
                   cost[0] = sum;
                   rank[0] = index;
                   max_heapify(0, k);
          }

          index++;

        }else if(input == 'T'){

           if(index < k)
             for(i=0; i<index; i++){
                print(rank[i]);
                if(i < index-1)
                    putchar_unlocked(' ');
              }

            else
             for(i=0; i<k; i++){
                print(rank[i]);
                if(i < k-1)
                    putchar_unlocked(' ');
              }

            putchar_unlocked('\n');        
        }

    }while(input == 'A' || input == 'T');

    return 0;
}
