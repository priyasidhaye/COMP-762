import java.awt.List;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.google.gson.Gson;

class ProductSearch {
	// This will display all the products in a given category specified by the
	// ids_{category}.json file

	// Also generated a huge JSON file containing products from all categories

	private static final String[] jsonFilePaths = { "./src/JSONfiles/ids_appliances.json",
			"./src/JSONfiles/ids_babieskids.json", "./src/JSONfiles/ids_cars.json",
			"./src/JSONfiles/ids_electronicsComputers.json", "./src/JSONfiles/ids_food.json",
			"./src/JSONfiles/ids_health.json", "./src/JSONfiles/ids_homeGarden.json", "./src/JSONfiles/ids_money.json" };

	public static void main(String[] args) throws IOException, ParseException {

		JSONParser jsonParser = new JSONParser();

		try {

			for (String s : jsonFilePaths) {
				FileReader fileReader = new FileReader(s);
				JSONArray jsonarray = (JSONArray) jsonParser.parse(fileReader);
				Gson gson = new Gson();

				FileWriter file = new FileWriter("./src/JSONfiles/ids_allProducts.json", true);

				for (int i = 0; i < jsonarray.size(); i++) {

					JSONObject jsonObject = (JSONObject) jsonarray.get(i);
					String h = jsonObject.toString();

					ProductsInfo p = gson.fromJson(h, ProductsInfo.class);

					// Generate a csv for all the products
					String data = p.getName() + "," + p.getId() + ","
							+ p.getDisplayName() + ";";

					file.write(data);

					// System.out.println(i + 1 + " name : " + p.getName() +"  id : "+ p.getId() + "  Display name : " + p.getDisplayName() + ";");

				}

				file.flush();
				file.close();
			}

		} finally {
			System.out.println("Done");

		}

	}

}