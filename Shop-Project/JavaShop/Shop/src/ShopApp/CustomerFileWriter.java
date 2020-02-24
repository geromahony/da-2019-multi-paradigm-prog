package ShopApp;

import java.io.IOException;
import java.io.PrintWriter;

public class CustomerFileWriter {

    public void toFile(String cName, double cBudget, String cProduct, int cQuantity){
        try {
            PrintWriter writer = new PrintWriter(cName + ".cust", "UTF-8");
            writer.println(cName + "," + String.format("%.2f", cBudget));
            writer.println(cProduct + "," + String.format("%d", cQuantity));
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}