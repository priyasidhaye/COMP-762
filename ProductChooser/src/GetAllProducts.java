import java.io.FileReader;
import java.util.*;
import java.io.IOException;
import java.util.HashMap;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import com.google.gson.Gson;

class GetAllProducts {

	class prodinfo {

		public String Name;
		public String id;
	}

	HashMap<String, prodinfo> allproducts = new HashMap<String, prodinfo>();

	public void getValues() throws IOException, ParseException {

		JSONParser jsonParser = new JSONParser();

		try {
			FileReader fileReader = new FileReader("./src/JSONfiles/id_allProducts.json");
			JSONArray jsonarray = (JSONArray) jsonParser.parse(fileReader);
			Gson gson = new Gson();

			for (int i = 0; i < jsonarray.size(); i++) {

				JSONObject jsonObject = (JSONObject) jsonarray.get(i);
				String h = jsonObject.toString();

				ProductsInfo p = gson.fromJson(h, ProductsInfo.class);

				System.out.println(i + 1 + "    Name : " + p.getName()
						+ "   Id : " + p.getId() + "    Display name :"
						+ p.getDisplayName());

				prodinfo value = new prodinfo();
				value.id = p.getId();
				value.Name = p.getName();
				allproducts.put(p.getDisplayName(), value);

			}

		} finally {
			System.out.println("Done");
		}

	}

	public void search(){
		
		
		Scanner scanner = new Scanner (System.in);
		System.out.print("Enter the full name of the product : ");  
		String userKey = scanner.nextLine(); // Get what the user types.
		
		if (allproducts.containsKey(userKey) == true){
	
			prodinfo value = allproducts.get(userKey);
			System.out.println("Key(Display Name): " + userKey +"  Product id : "+ value.id+" Name : "+ value.Name);
		}
	}
	public static void main(String[] args) throws IOException, ParseException {

		GetAllProducts getallproducts = new GetAllProducts();

		getallproducts.getValues();
		getallproducts.search();

	}

}