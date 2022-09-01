import java.util.ArrayList;

public class RunDealers {
    public static void main(String[] args) {
        Dealer d1 = new Dealer("Dan the Dealer");
        d1.addBidInfo(95.0, 100);
        d1.addBidInfo(94.0, 40);
        d1.addBidInfo(93.0, 15);
        d1.addBidInfo(92.0, 5);
        d1.addAskInfo(105.0, 120);
        d1.addAskInfo(106.0, 50);
        d1.addAskInfo(107.0, 20);
        d1.printDealerInfo();

        Trader tim = new Trader("Tim");
        ArrayList<ArrayList<Object>> timTrades = new ArrayList<>();
        timTrades.add(tim.trade(95.0, 10, 1));
        timTrades.add(tim.trade(100.0, 5, 0));
        timTrades.add(tim.trade(104.0, 8, 0));
        for(ArrayList<Object> s: timTrades){
            d1.trade(s);
            d1.adjustToTrade(s);
            d1.adjustToInventory();
            d1.adjustToCosts();
            d1.printDealerInfo();
        }
    }
}