package ShopApp;

import java.util.List;
import java.util.Scanner;

public class Runner {

	public static void main(String[] args) {

		int queueCleared = 0;

		Shop shop = new Shop("src/ShopApp/stock.csv");
		Scanner scan = new Scanner(System.in);

		System.out.println("Welcome to the shop, Whats your name?");
		String customerName = scan.nextLine();

		while (true){
			Scanner scanWhile = new Scanner(System.in);

			System.out.println("=================================================");
			System.out.println("| Please select an option:                      |");
			System.out.println("| ------------------------                      |");
			System.out.println("| Allow the customer queue to go ahead:     [1] |");
			System.out.println("| Buy something yourself:                   [2] |");
			System.out.println("| Leave the shop:                           [3] |");
			System.out.println("| Print shop details:                       [4] |");
			System.out.println("=================================================");

			String answer = scanWhile.nextLine();

			switch(answer){
				case "1":
					if( queueCleared > 0){
						System.out.println("The customer queue has alredy been served\n");
					} else {
						List<String> fileList = new CustomerFileFinder().inputFileinDir("src/ShopApp/customers/");
						for (String item : fileList) {
							Customer nextCustomer = new Customer("src/ShopApp/customers/" + item);
							// System.out.println(nextCustomer);
							shop.processOrder(nextCustomer);
							queueCleared = 1;
							System.out.println("=============================================\n");
					}
					continue;
				}

				case "2":
					// ask the user for what they want to buy and save as string
					System.out.println("What product do you want to buy?");
					List <ProductStock> currentStockList = shop.getStock();
					for (ProductStock listItem : currentStockList) {
						System.out.println(listItem.getProduct().getName());
					}
					System.out.println("=============================================\n");
					String productName = scanWhile.nextLine();

					// Ask how many they want and save as a integer
					System.out.println("How many " + productName + " do you want?");
					int amount = scanWhile.nextInt();

					// find out how much money they have to pay you with
					System.out.println("What's your budget today?");
					double cash = scanWhile.nextDouble();

					CustomerFileWriter fw = new CustomerFileWriter();
					fw.toFile(customerName, cash, productName, amount);
					Customer localCustomer = new Customer(customerName +".cust");
					shop.processOrder(localCustomer);
					continue;

				case "3":
					System.out.println("Thank you for your custom, please call again!\n Godbye \n");
					scanWhile.close();
					scan.close();
					return;

				case "4":
					System.out.println(shop);
					continue;

				default:
					scanWhile.close();
					break;
			}
			scan.close();		
		}
	}
}
