import java.io.FileReader;
import java.util.*;
import java.io.IOException;
import java.util.HashMap;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import com.google.gson.Gson;

import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;
class GetAllProducts {

	class prodinfo {

		public String Name;
		public String id;
	}

	HashMap<String, prodinfo> allproducts = new HashMap<String, prodinfo>();
	
	// Lucene stuff
	private Directory index;
	private final int MAX_NUM_RESULTS = 10;
	private final static boolean SEARCH_WITH_LUCENE = true;

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
		String userinput= "";
		while(!userinput.equals("exit")) {
			System.out.print("Enter the full name of the product (or 'exit'): ");  
			userinput = scanner.nextLine(); // Get what the user types.
			
			if (SEARCH_WITH_LUCENE) {
				luceneSearch(userinput);
			} else if (allproducts.containsKey(userinput)){
				prodinfo value = allproducts.get(userinput);
				System.out.println("Key(Display Name): " + userinput +"  Product id : "+ value.id+" Name : "+ value.Name);
			}
			
		}
		scanner.close();
	}
	public static void main(String[] args) throws IOException, ParseException {

		GetAllProducts getallproducts = new GetAllProducts();

		getallproducts.getValues();
		
		if (SEARCH_WITH_LUCENE) {
			getallproducts.setupIndex();
		}
		
		getallproducts.search();

	}
	
	public void setupIndex() {
		try {
			index = new RAMDirectory();
			IndexWriter writer = new IndexWriter(index, new IndexWriterConfig(Version.LUCENE_46,new EnglishAnalyzer(Version.LUCENE_46)));
		
		for (String productname : allproducts.keySet()) {
			// System.out.println("adding : " + productname);
			Document doc = new Document();
			doc.add(new TextField("name", productname, Field.Store.YES));
			// TODO: Right now I'm just adding the names in the lucene index, 
			// but we should add all fields for all products, not just the name!
			writer.addDocument(doc);
		}
		writer.close();
		} catch (IOException e) {
			System.out.println(e);
		}
	}
	
	public void luceneSearch(String querystr) {
		try {
			Query q = new QueryParser(Version.LUCENE_46, "name", new EnglishAnalyzer(Version.LUCENE_46)).parse(querystr);
			
			IndexReader reader = IndexReader.open(index);
			IndexSearcher searcher = new IndexSearcher(reader);
			TopScoreDocCollector results = TopScoreDocCollector.create(MAX_NUM_RESULTS, true);
			searcher.search(q, results);
			ScoreDoc[] hits = results.topDocs().scoreDocs;
			
			System.out.println("Found " + hits.length + " results.");
			for(int i=0; i<hits.length; i++) {
			    int docId = hits[i].doc;
			    Document doc = searcher.doc(docId);
			    System.out.println((i + 1) + ". " + doc.get("name"));
			}
		} catch (Exception e) {
			System.out.println(e);
		}
	}

}