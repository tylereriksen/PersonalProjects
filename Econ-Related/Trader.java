import java.util.ArrayList;
import java.text.SimpleDateFormat;  
import java.util.Date;  

public class Trader{
    String name;

    // constructor
    Trader(String name){
        this.name = name;
    }

    /*
    * get the name
    * @preturn String name
    */
    String getName() {
        return this.name;
    }

    ArrayList<Object> trade(double limit, int quantity, int buy_or_sell){
        ArrayList<Object> returnList = new ArrayList<>();
        returnList.add(this.getName());
        returnList.add(limit);
        returnList.add(quantity);
        if(buy_or_sell == 0){returnList.add("Buy");}
        else if(buy_or_sell == 1){returnList.add("Sell");}
        SimpleDateFormat formatter = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
        Date date = new Date();  
        returnList.add(formatter.format(date));
        return returnList;
    }

}