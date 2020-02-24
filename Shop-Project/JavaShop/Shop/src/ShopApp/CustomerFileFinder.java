package ShopApp;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class CustomerFileFinder {
    // Class for finding customer files in a directory
    List<String> inputFileinDir(String directory) {
        List<String> inputFileinDir = new ArrayList<String>();
        File dir = new File(directory);
        for (File file : dir.listFiles()) {
            if (file.getName().endsWith((".cust"))) {
                inputFileinDir.add(file.getName());
            }
        }
        return inputFileinDir;
    }
}