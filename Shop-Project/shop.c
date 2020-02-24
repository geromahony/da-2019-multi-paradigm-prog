#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <dirent.h>
#include <stdbool.h>
#include <math.h>

struct Product {
	char* name;
	double price;
};

struct ProductStock {
	struct Product product;
	int quantity;
};

struct Shop {
	double cash;
	struct ProductStock stock[20];
	int index;
};

struct Customer {
	char* name;
	double budget;
	struct ProductStock shoppingList[10];
	int index;
};

struct CustomerQueue {
	struct Customer customerQ[20];
	int index;
};

void printProduct(struct Product p)
{
	printf("%s, Price: €%.2f, ", p.name, p.price);
}

void printCustomer(struct Customer c)
{
	printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f\n", c.name, c.budget);
	printf("-------------\n");
	int i;
	for( i = 0; i < c.index; i++)
	{
		printProduct(c.shoppingList[i].product);
		printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity);
		double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price; 
		printf("The cost to %s will be €%.2f\n", c.name, cost);
	}
	printf("\n");
}

struct Shop createAndStockShop()
{

	// struct Shop shop;
	struct Shop shop = { 200 };

	FILE *fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    getline(&line, &len, fp);

    shop.cash = atof(line);

    while ((read = getline(&line, &len, fp)) != -1) 
	{
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");
		int quantity = atoi(q);
		double price = atof(p);
		char *name = malloc(sizeof(char) * 50);
		strcpy(name, n);
		struct Product product = { name, price };
		struct ProductStock stockItem = { product, quantity };
		shop.stock[shop.index++] = stockItem;
    }
    fclose(fp);
	
	return shop;
}

void printShop(struct Shop* s)
{
	printf("Shop: \n Cash=€%.2f\n Stock:\n", s->cash);
	int i;
	for ( i = 0; i < s->index; i++)
	{
		printProduct(s->stock[i].product);
		printf("Quantity: %d\n", s->stock[i].quantity);
	}
}


struct Customer processCustomer(char *fileName)
{
	FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
	char customerDirFileName[255] = "./customers/";
	strcat(customerDirFileName,fileName);

	fp = fopen(customerDirFileName, "r");
	if (fp == NULL)
      exit(EXIT_FAILURE);

	// Get customer Name and budget from first line
	getline(&line, &len, fp);
	
	// Use string token function to split CSV values
	// into name n and cash c string values
	char *n = strtok(line, ",");
	char *c = strtok(NULL, ",");

	char *name = malloc(sizeof(char) * 50);
	strcpy(name, n);

	double cash = atof(c);

	struct Customer newCustomer = { name, cash };

    while ((read = getline(&line, &len, fp)) != -1)
    {
    	char *p = strtok(line, ",");
		char *q = strtok(NULL, ",");
		int quantity = atoi(q);

		char *productName = malloc(sizeof(char) * 50);
		strcpy(productName, p);
		struct Product product = { productName };
		struct ProductStock stockItem = { product, quantity };
		newCustomer.shoppingList[newCustomer.index++] = stockItem;
    }
    
	fclose(fp);

	return newCustomer;
}

struct CustomerQueue queueCustomers()
{
	struct CustomerQueue queue = {.index = 0};
	size_t flen;
	DIR *customerDir;
	struct  dirent *file;
	char customerFileName[255];
	customerDir = opendir("./customers");
	if (customerDir)
	{
		while ((file = readdir(customerDir)) != NULL)
		{
			strncpy(customerFileName, file->d_name, 254);
			customerFileName[254] = '\0';

			if (strstr(customerFileName, ".cust") != NULL)
			{
				struct Customer newCustomer = processCustomer(customerFileName);
				queue.customerQ[queue.index++] = newCustomer;
			}
		}
		closedir(customerDir);
	}
	return queue;
}

void printQueue(struct CustomerQueue q)
{
	printf("The queue has %d customers\n", q.index);
	int i;
	for (i = 0; i < q.index; i++)
	{
		printCustomer(q.customerQ[i]);
	}
}

void serveCustomer(struct Shop* s, struct CustomerQueue* c, bool q)
{
	int stockQuantity;
	int stockIndex;
	double itemPrice;
	double costToCust;
	double remainingBudget;

	int iCust;
	for (iCust = 0; iCust < c->index; iCust++)
	{
		printf("=============================================\n");
		if(q)
		{
			printf("Hello %s how can I help you today?\n", c->customerQ[iCust].name);
		}

		int iList;
		for (iList = 0; iList < c->customerQ[iCust].index; iList++)
		{
			printf("You want %d of %s\n",
				   c->customerQ[iCust].shoppingList[iList].quantity,
				   c->customerQ[iCust].shoppingList[iList].product);

			stockIndex = checkProductStock(s, c, &iCust, &iList, &stockQuantity, &itemPrice);
			if (stockQuantity <= c->customerQ[iCust].shoppingList[iList].quantity)
			{
				printf("Sorry %s, we don't have enough stock to fulfill your order\n", c->customerQ[iCust].name);
			} else if (stockQuantity > 0) {
				printf("We have %d of %s which cost €%.2f each\n", stockQuantity,
					   c->customerQ[iCust].shoppingList[iList].product.name, itemPrice);
				costToCust = itemPrice * c->customerQ[iCust].shoppingList[iList].quantity;
				printf("%d of %s will cost you: \n",
					   c->customerQ[iCust].shoppingList[iList].quantity,
					   c->customerQ[iCust].shoppingList[iList].product);
				printf("€%.2f\n", costToCust);
				remainingBudget = c->customerQ[iCust].budget - costToCust;

				if (remainingBudget >= 0.0)
				{
					printf("You have €%.2f left in your €%.2f budget\n", remainingBudget,c->customerQ[iCust].budget);
					c->customerQ[iCust].budget = remainingBudget;
					reduceProductStock(s, &stockIndex,
									   c->customerQ[iCust].shoppingList[iList].product.name,
									   c->customerQ[iCust].shoppingList[iList].quantity);
					s->cash = s->cash + costToCust;
				}
				else
				{
					printf("Sorry %s, you don't have enough money to purchase %d of %s\n",
						   c->customerQ[iCust].name,
						   c->customerQ[iCust].shoppingList[iList].quantity,
						   c->customerQ[iCust].shoppingList[iList].product);
					continue;
				}
			} else {
				printf("Sorry %s, we are out of stock for %s\n",
					   c->customerQ[iCust].name, c->customerQ[iCust].shoppingList[iList].product.name);
			}
		}
	}
}

int checkProductStock(struct Shop* s, struct CustomerQueue* c, int *iCust, int *iList, int *quantity, double *price)
{
	int compare;
	int i;
	for (i=0; i < s->index; i++)
	{
		compare = compare_string(s->stock[i].product.name, 
		c->customerQ[*iCust].shoppingList[*iList].product.name);
		if (compare == 0)
		{
			*quantity = s->stock[i].quantity;
			*price = s->stock[i].product.price;
			return i;
		}
	}
	*quantity = -1;
	*price = 0.0;
	return -1;
}

int reduceProductStock(struct Shop *s, int *stockIndex, char *customerProduct, int customerQuantity)
{
	int compare;
	compare = compare_string(s->stock[*stockIndex].product.name, customerProduct);
	if (compare == 0)
	{
		s->stock[*stockIndex].quantity = s->stock[*stockIndex].quantity - customerQuantity;
		return 1;
	}
	return 0;
}

int compare_string(char *first, char *second)
{
	while (*first == *second)
	{
		if (*first == '\0' || *second == '\0')
			break;

		first++;
		second++;
	}
	if (*first == '\0' && *second == '\0')
		return 0;
	else
		return -1;
}

int checkUserInput()
{
	int n;
	double temp;

	char value[MAX_INPUT] = "0";
	char str[MAX_INPUT] = "";

	// Precision for integer checking
	double val = 1e-12;

	fgets(value, 255, stdin); // Read input

	// Check for integers.
	if (sscanf(value, "%lf", &temp) == 1)
	{
		n = (int)temp; // typecast to int.
		if (fabs(temp - n) / temp > val)
		{
			printf("Please enter an integer number\n");
			return 0;
		} else {
			return n;
		}
	} else if (sscanf(value, "%s", str) == 1) {
		printf("Please enter an integer number\n");
		return 0;
	} else {
		printf("Please enter an integer number\n");
		return 0;
	}	
}

void serveCounter(struct Shop* s, char *name)
{
	struct CustomerQueue counterQ = {};
	int productIndex=0;
	char term;
	char *productName = malloc(sizeof(char) * 50);
	int quantity;
	double budget;
	
	printf("Hello %s\n", name);
	printf("Please select something from our stocklist: \n");
	printf("+++++++++++++++++++++++++++++++++++++++++++++\n");
	int i;
	for (i = 0; i < s->index; i++)
	{
		printf("[%d]: %s\n", i+1, s->stock[i].product);
	}
	printf("+++++++++++++++++++++++++++++++++++++++++++++\n");

	while(true)
	{
		productIndex = checkUserInput();

		if (productIndex > s->index+1)
		{
			printf("Please select a product index from the list\n");
			continue;
		} else if (productIndex == 0){
			continue;

		} else {
			printf("+++++++++++++++++++++++++++++++++++++++++++++\n");
			break;
		}
	}
	productIndex = productIndex -1;

	strcpy(productName, s->stock[productIndex].product.name);

	printf("What amount of %s would you like?\n", productName );
	scanf("%d", &quantity);

	printf("What's your budget today %s?\n", name);
	scanf("%lf", &budget);

	struct Customer counterCustomer = {
		.name = name,
		.budget = budget,
		.index = 0};

	struct Product product = {productName};
	struct ProductStock stockItem = {product, quantity};
	counterCustomer.shoppingList[counterCustomer.index++] = stockItem;

	counterQ.customerQ[counterQ.index++] = counterCustomer;

	serveCustomer(s, &counterQ, false);
}

int main(void) 
{
	struct Shop shop = createAndStockShop();
	struct CustomerQueue queue = queueCustomers();

	int answer;
	int queueCleared = 0;
	char customerName[256];
	char *name;

	printf("Welcome to the shop. What's your name?\n");
	scanf("%s", &customerName);
	name = customerName;

	while (1)
	{
		printf("=================================================\n");
		printf("| Please select an option:                      |\n");
		printf("| ------------------------                      |\n");
		printf("| Allow the customer queue to go ahead:     [1] |\n");
		printf("| Buy something yourself:                   [2] |\n");
		printf("| Leave the shop:                           [3] |\n");
		printf("| Print shop details:                       [4] |\n");
		printf("=================================================\n");
		scanf("%d", &answer);
		switch(answer)
		{
			case 1:
				if (queueCleared == 0)
				{
					serveCustomer(&shop, &queue, true);
					queueCleared = 1;
				} else {
					printf("The customer queue has alredy been served\n");
				}
				continue;

			case 2:
				serveCounter(&shop, name);
				continue;

			case 3:
				printf("Thank you for your custom, please call again!\n");
				printf("Goodbye\n");
				return;

			case 4:
				printShop(&shop);
				continue;

			default:
				return -1;
		}
	}
	
    return 0;
}