package ShopApp;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Shop {

	private double cash;
	private ArrayList<ProductStock> stock;

	public Shop(String fileName) {
		stock = new ArrayList<>();
		List<String> lines = Collections.emptyList();
		try {
			lines = Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8);
			System.out.println(lines.get(0));
			cash = Double.parseDouble(lines.get(0));
			// i am removing at index 0 as it is the only one treated differently
			lines.remove(0);
			for (String line : lines) {
				String[] arr = line.split(",");
				String name = arr[0];
				double price = Double.parseDouble(arr[1]);
				int quantity = Integer.parseInt(arr[2].trim());
				Product p = new Product(name, price);
				ProductStock s = new ProductStock(p, quantity);
				stock.add(s);
			}
			
		}

		catch (IOException e) {

			// do something
			e.printStackTrace();
		}
	}

	public double getCash() {
		return cash;
	}

	public ArrayList<ProductStock> getStock() {
		return stock;
	}

	@Override
	public String toString() {
		String retn = "Shop: \n Cash=" + String.format("%.2f", cash) + "\n Stock: \n";
		for (ProductStock item : stock) {
			retn+= item.getProduct().getName() + ", Price: €" + 
				String.format("%.2f", item.getProduct().getPrice()) +
				", Quantity: " + item.getQuantity() +  "\n";
		}
		return retn;
	}

	public static void main(String[] args) {
		// Shop shop = new Shop("src/ShopApp/stock.csv");
	}
	
	private double findPrice(String name) {
		
		for (ProductStock productStock : stock) {
			Product p =productStock.getProduct();
			if (p.getName().equals(name)) {
				return p.getPrice();
			}
		}
		
		return -1;
	}
	
	public void processOrder(Customer c) {
		ArrayList<ProductStock> custList = c.getShoppingList();

		System.out.println("Hello " + c.getName() + " how can I help you today? \n");
		System.out.println("=============================================");

		CUSTOMER_LOOP:
		for (ProductStock listItem : custList) {

			System.out.println("\n");

			System.out.println("You want " + listItem.getQuantity() + " of " + listItem.getProduct().getName());

			for (ProductStock productStock : stock) {
			Product p = productStock.getProduct();	

				if(p.getName().equals(listItem.getProduct().getName())){
					int quantity = productStock.getQuantity();
					double price = findPrice(p.getName());
					double costToCustomer = price * listItem.getQuantity();
					double remainingBudget = c.getBudget() - costToCustomer;

					System.out.println("We have " + quantity +
					" of " + p.getName() + " which will cost €" + String.format("%.2f", price) + " each");
					System.out.println(listItem.getQuantity() + " of " + p.getName() + " will cost you: €" + String.format("%.2f", costToCustomer));

					if(quantity >= listItem.getQuantity()){
						
						if( costToCustomer <= c.getBudget()){
							// Customer can afford item
							System.out.println("You have €" + String.format("%.2f", remainingBudget) + " left of your €"
									+ String.format("%.2f", c.getBudget()) + " budget");
							// Reduce their budget accordingly
							c.setBudget(remainingBudget);
							// Reduce shop stock
							productStock.setQuantity(quantity - listItem.getQuantity());
							// Add to shop balance
							cash = cash + costToCustomer;
							
							continue CUSTOMER_LOOP;
						} else {
							// Customer cannot afford item
							System.out.println("Sorry " + c.getName() + 
							", you don't have enough money to purchase " + listItem.getQuantity()
							+ " of " + listItem.getProduct().getName() );
						}
					} else if (quantity == 0){
						// No stock in shop
						System.out.println("Sorry " + c.getName() + 
						", we are out of stock for " + listItem.getProduct().getName() );
						continue CUSTOMER_LOOP;
					}else {
						// Not enough stock in shop
						System.out.println("Sorry " + c.getName() + 
						", we don't have enough stock to fulfill your order ");
						continue CUSTOMER_LOOP;
					}
				}
			}
		}
	}
}
