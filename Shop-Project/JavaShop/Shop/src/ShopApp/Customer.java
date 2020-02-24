package ShopApp;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Customer {
	// Customer class
	
	// Class members
	private String name;
	private double budget;
	private ArrayList<ProductStock> shoppingList;
	
	// Class method to initalise customer
	public Customer(String fileName) {
		
		shoppingList = new ArrayList<>();
		List<String> lines = Collections.emptyList();
		try {
			lines = Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8);
			String[] firstLine = lines.get(0).split(",");
			name = firstLine[0];
			budget = Double.parseDouble(firstLine[1]);
			lines.remove(0);
			for (String line : lines) {
				String[] arr = line.split(",");
				String name = arr[0];
				int quantity = Integer.parseInt(arr[1].trim());
				Product p = new Product(name, 0);
				ProductStock s = new ProductStock(p, quantity);
				shoppingList.add(s);
			}
			
		}

		catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public String getName() {
		return name;
	}


	public double getBudget() {
		return budget;
	}

	public void setBudget(double budget){
		this.budget = budget;
	}


	public ArrayList<ProductStock> getShoppingList() {
		return shoppingList;
	}


	@Override
	public String toString() {
		String ret = "Customer: \n Name: " + name + "\n Budget: " + String.format("%.2f", budget) + "\n ShoppingList: \n";
		for (ProductStock productStock : shoppingList) {
			ret+= productStock.getProduct().getName() + " Quantity: " + productStock.getQuantity() + "\n";
		}
		return ret;
	}

}
