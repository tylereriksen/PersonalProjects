import java.util.ArrayList;

public class RunDealers {
    public static void main(String[] args) {
        Dealer d1 = new Dealer();
        d1.addBidInfo(95.0, 100);
        d1.addBidInfo(94.0, 40);
        d1.addBidInfo(93.0, 15);
        d1.addBidInfo(92.0, 5);
        d1.addAskInfo(105.0, 120);
        d1.addAskInfo(106.0, 50);
        d1.addAskInfo(107.0, 20);
        d1.printDealerInfo();
        Trader tim = new Trader("Tim");
        ArrayList<Object> timTrade1 = tim.trade(95.0, 10, 1);
        d1.trade(timTrade1);
        d1.adjustToTrade();
        d1.printDealerInfo();
        ArrayList<Object> timTrade2 = tim.trade(95.0, 5, 0);
        d1.trade(timTrade2);
        d1.adjustToTrade();
        d1.printDealerInfo();
        ArrayList<Object> timTrade3 = tim.trade(101.0, 8, 0);
        d1.trade(timTrade3);
        d1.adjustToTrade();
        d1.printDealerInfo();
    }
}