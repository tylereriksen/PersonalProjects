import java.util.ArrayList;
import java.util.Random;

public class Dealer {

    /*
    * Instance Variables for the Dealer class
    */
    ArrayList<Double> bid = new ArrayList<Double>();
    ArrayList<Double> ask = new ArrayList<Double>();
    ArrayList<Integer> bidSize = new ArrayList<Integer>();
    ArrayList<Integer> askSize = new ArrayList<Integer>();
    String name;
    int inventory;
    int last_inv;
    private double tick = 1.0;

    // the constructor
    public Dealer(String name){
        this.name = name;
        this.inventory = 0;
        this.last_inv = 0;
    }

    /*
    * get the bid price ArrayLists
    * @return Double ArrayList of bid prices
    */
    ArrayList<Double> getBidPrices() {return this.bid;}

    /*
    * get the ask price ArrayLists
    * @return Double ArrayList of ask prices
    */
    ArrayList<Double> getAskPrices() {return this.ask;}

    /*
    * get the bid size ArrayLists
    * @return Integer ArrayList of bid sizes
    */
    ArrayList<Integer> getBidSizes() {return this.bidSize;}

    /*
    * get the ask size ArrayLists
    * @return Integer ArrayList of ask sizes
    */
    ArrayList<Integer> getAskSizes() {return this.askSize;}

    /*
    * Method to check if there are duplicate quotation prices and if there are 
    * quotations of size 0 and delete them and combine them in appropriate ways
    * @param int i - 0 to check bids and 1 to check asks
    */
    private void checkQuotations(int i){
        if(i == 0){
            int limit = this.bid.size();
            for(int j = 0; j < limit - 1; j++){
                if(this.bid.get(j) == this.bid.get(j + 1)){
                    Double del_bid = this.bid.get(j + 1);
                    int del_bidSize = this.bidSize.get(j + 1);
                    this.bid.remove(j + 1);
                    this.bidSize.remove(j + 1);
                    this.bid.set(j, this.bid.get(j) + del_bid);
                    this.bidSize.set(j, this.bidSize.get(j) + del_bidSize);
                    break;
                }
            }
            limit = this.bid.size();
            for(int j = 0; j < limit; j++){
                if(this.bidSize.get(j) == 0.0){
                    this.bid.remove(j);
                    this.bidSize.remove(j);
                    break;
                }
            }
        }
        else{
            int limit = this.ask.size();
            for(int j = 0; j < limit - 1; j++){
                if(this.ask.get(j) == this.ask.get(j + 1)){
                    Double del_ask = this.ask.get(j + 1);
                    int del_askSize = this.askSize.get(j + 1);
                    this.ask.remove(j + 1);
                    this.askSize.remove(j + 1);
                    this.ask.set(j, this.ask.get(j) + del_ask);
                    this.askSize.set(j, this.askSize.get(j) + del_askSize);
                    break;
                }
            }
            limit = this.ask.size();
            for(int j = 0; j < limit; j++){
                if(this.askSize.get(j) == 0.0){
                    this.ask.remove(j);
                    this.askSize.remove(j);
                    break;
                }
            }
        }
    }

    /*
    * gets additional bid price and bid size at that price and adds it to the 
    * respective instance variables
    * @param double price - bid price
    * @ param int size - size at bid price
    */
    void addBidInfo(double price, int size){
        if(this.ask.size()  != 0 && price > this.ask.get(0)){
            throw new IllegalArgumentException("This cannot be a Bid Price!");
        }
        if (this.bid.size() == 0) {
            this.bid.add(price);
            this.bidSize.add(size);
        }
        else {
            int limit = this.bid.size();
            for (int i = 0; i < limit; i++) {
                if (this.bid.get(i) < price) {
                    this.bid.add(i, price);
                    this.bidSize.add(i, size);
                    break;
                }
                else if(i == this.bid.size() - 1){
                    this.bid.add(price);
                    this.bidSize.add(size);
                }
            }
            this.checkQuotations(0);
        }
    }

    /*
    * prints out the bid price and size information
    */
    private void printBidInfo(){
        System.out.println(this.name + "'s Current Bids are: ");
        for(int i = 0; i < this.bid.size(); i++){
            System.out.println(this.bidSize.get(i) + " bid at " + this.bid.get(i));
        }
    }

    /*
    * gets additional ask price and ask size at that price and adds it to the 
    * respective instance variables
    * @param double price - ask price
    * @ param int size - size at ask price
    */
    void addAskInfo(double price, int size){
        if (this.bid.size() != 0 && price < this.bid.get(0)){
            throw new IllegalArgumentException("This cannot be a Ask Price!");
        }
        if (this.ask.size() == 0){
            this.ask.add(price);
            this.askSize.add(size);
        }
        else {
            int limit = this.ask.size();
            for(int i = 0; i < limit; i ++){
                if (this.ask.get(i) > price) {
                    this.ask.add(i, price);
                    this.askSize.add(i, size);
                    break;
                }
                else if(i == this.ask.size() - 1){
                    this.ask.add(price);
                    this.askSize.add(size);
                }
            }
            this.checkQuotations(1);
        }
    }

    /*
    * prints out the ask price and size information
    */
    private void printAskInfo(){
        System.out.println(this.name + "'s Current Asks are: ");
        for(int i = 0; i < this.ask.size(); i++){
            System.out.println(this.askSize.get(i) + " ask at " + this.ask.get(i));
        }
    }

    /*
    * prints out both the bid and ask prices and sizes information
    */
    void printDealerInfo(){
        this.printBidInfo();
        System.out.println();
        this.printAskInfo();
        System.out.println();
        if(this.inventory > 0){
            System.out.println("Dealer Inventory: Long " + this.inventory);
        }
        else if(this.inventory < 0){
            System.out.println("Dealer Inventory: Short " + Math.abs(this.inventory));
        }
        else{
            System.out.println("Dealer Inventory: Balanced");
        }
        System.out.println();
        System.out.println("------------------------------------------------------------------------------------");
        System.out.println();
    }

    /*
    * change one of the current bid prices to a new bid price
    * @param double price - the bid price that will be changed
    * @param double newPrice - the new bid price
    */
    void changeBidPrice(double price, double newPrice){
        if (this.bid.contains(price) == false){
            throw new IllegalArgumentException("Bid Price must have been already quoted!");
        }
        int idx = 0;
        for(int i = 0; i < this.bid.size(); i ++){
            idx = i;
            if(this.bid.get(i) == price){
                break;
            }
        }
        this.bid.set(idx, newPrice);
        this.checkQuotations(0);
    }

    /*
    * change the bid size at a certain bid price
    * @param double price - the bid price that will have size changed
    * @param int size - the new bid size at price
    */
    void changeBidQuotation(double price, int size){
        if (this.bid.contains(price) == false){
            throw new IllegalArgumentException("Bid Price must have been already quoted!");
        }
        int idx = 0;
        for(int i = 0; i < this.bid.size(); i ++){
            idx = i;
            if(this.bid.get(i) == price){
                break;
            }
        }
        this.bidSize.set(idx, size);
        this.checkQuotations(0);
    }

    /*
    * change one of the current ask prices to a new ask price
    * @param double price - the ask price that will be changed
    * @param double newPrice - the new ask price
    */
    void changeAskPrice(double price, double newPrice){
        if (this.ask.contains(price) == false){
            throw new IllegalArgumentException("Ask Price must have been already quoted!");
        }
        int idx = 0;
        for(int i = 0; i < this.ask.size(); i ++){
            idx = i;
            if(this.ask.get(i) == price){
                break;
            }
        }
        this.ask.set(idx, newPrice);
        this.checkQuotations(1);
    }

    /*
    * change the ask size at a certain ask price
    * @param double price - the ask price that will have size changed
    * @param int size - the new ask size at price
    */
    void changeAskQuotation(double price, int size){
        if (this.ask.contains(price) == false){
            throw new IllegalArgumentException("Ask Price must have been already quoted!");
        }
        int idx = 0;
        for(int i = 0; i < this.ask.size(); i ++){
            idx = i;
            if(this.ask.get(i) == price){
                break;
            }
        }
        this.askSize.set(idx, size);
        this.checkQuotations(1);
    }

    /*
    * takes a trade and updates the bid or ask size and/or prices with the trade
    * @param Object ArrayList tradeDetails - trade from Trader class method
    */
    // LOOK AT THIS ONE AGAIN
    void trade(ArrayList<Object> tradeDetails){
        if(!(tradeDetails.get(0) instanceof String) ||
           !(tradeDetails.get(1) instanceof Double) ||
           !(tradeDetails.get(2) instanceof Integer) ||
           !(tradeDetails.get(3) instanceof String) ||
           !(tradeDetails.get(4) instanceof String) ||
           tradeDetails.size() != 5){throw new IllegalArgumentException("Please Enter a Valid Trade Information.");}
        int idx = 0;
        if(tradeDetails.get(3) == "Sell"){
            idx = this.bid.indexOf(tradeDetails.get(1));
            if(idx == -1){
                throw new ArrayIndexOutOfBoundsException("This Offer is not in the Dealer's Quotations.");
            }
            if(this.bidSize.get(idx) >= (int)tradeDetails.get(2)){
                int currentSize = this.bidSize.get(idx);
                this.changeBidQuotation((double)tradeDetails.get(1), currentSize + (int)tradeDetails.get(2));
                this.inventory += (int)tradeDetails.get(2);
            }
        }

        else if(tradeDetails.get(3) == "Buy"){
            idx = this.ask.indexOf(tradeDetails.get(1));
            if(idx == -1){
                throw new ArrayIndexOutOfBoundsException("This Offer is not in the Dealer's Quotations.");
            }
            if(this.askSize.get(idx) >= (int)tradeDetails.get(2)){
                int currentSize = this.askSize.get(idx);
                this.changeAskQuotation((Double)tradeDetails.get(1), currentSize - (int)tradeDetails.get(2));
                this.inventory -= (int)tradeDetails.get(2);
            }
        }
        System.out.println("Traded with " + tradeDetails.get(0) + " who offers to " + tradeDetails.get(3) + " " + tradeDetails.get(2) + " for " + tradeDetails.get(1) + " at " + tradeDetails.get(4) + ".");
        String buy_or_sell;
        if(tradeDetails.get(3) == "Buy"){buy_or_sell = "Sold";}
        else if(tradeDetails.get(3) == "Sell"){buy_or_sell = "Bought";}
        else{throw new IllegalArgumentException("Wrong Object in Trade Details.");}
        System.out.println(tradeDetails.get(4) + " Trade Summary: " + buy_or_sell + " " + tradeDetails.get(2) + " for " + tradeDetails.get(1) + " from " + tradeDetails.get(0));
        System.out.println();
    }

    /*
    * change the bid and ask prices and sizes according to inventory size
    */
    void adjustToInventory(){
        Random rand = new Random();
        int j = rand.nextInt(10);
        if(j > 0){
            for(int i = 0; i < this.bid.size(); i++){
                this.changeBidPrice(this.bid.get(i), this.bid.get(i) - this.tick * (int)(0.4 * (this.inventory - this.last_inv)));
            }
            for(int i = 0; i < this.ask.size(); i++){
                this.changeAskPrice(this.ask.get(i), this.ask.get(i) - this.tick * (int)(0.4 * (this.inventory - this.last_inv)));
            }
            this.last_inv = this.inventory;
        }
        else if(j == 0){
            for(int i = 0; i < this.bidSize.size(); i++){
                if(this.inventory - this.last_inv >= 0){
                    this.changeBidQuotation(this.bid.get(i), (int)(this.bidSize.get(i) * Math.min(1.3, 1.0 + (0.03 * (this.inventory - this.last_inv)))));
                }
                else{
                    this.changeBidQuotation(this.bid.get(i), (int)(this.bidSize.get(i) * Math.max(0.7, 1.0 - (0.03 * (this.inventory - this.last_inv)))));
                }
            }
            for(int i = 0; i < this.askSize.size(); i++){
                if(this.inventory - this.last_inv >= 0){
                    this.changeAskQuotation(this.ask.get(i), (int)(this.askSize.get(i) * Math.max(0.7, 1.0 - (0.03 * (this.inventory - this.last_inv)))));
                }
                else{
                    this.changeAskQuotation(this.ask.get(i), (int)(this.askSize.get(i) * Math.min(1.3, 1.0 + (0.03 * (this.inventory - this.last_inv)))));
                }
            }
        }
    }

    /*
    * change the bid and ask prices and sizes according to the trade
    * @param Object ArrayList tradeDetails - trade that happened
    */
    void adjustToTrade(ArrayList<Object> tradeDetails){
        int sign = 0;
        if(tradeDetails.get(3) == "Buy"){sign = 1;}
        else{sign = -1;}
        for(int i = 0; i < this.bid.size(); i ++){
            this.bid.set(i, this.bid.get(i) + sign * this.tick);
        }
        for(int i = 0; i < this.ask.size(); i ++){
            this.ask.set(i, this.ask.get(i) + sign * this.tick);
        }

    }

    /*
    * get the inside spread from a number of dealers
    * @param ArrayList<Dealer> dealerList - list of different dealers
    * @return double difference between best bid and best ask from all the dealers
    */
    double insideSpread(ArrayList<Dealer> dealerList){
        double bestBid = this.bid.get(0);
        double bestAsk = this.ask.get(0);
        for(int i = 0; i < dealerList.size(); i++){
            if(dealerList.get(i).getBidPrices().get(0) > bestBid){
                bestBid = dealerList.get(i).getBidPrices().get(0);
            }
            if(dealerList.get(i).getAskPrices().get(0) < bestAsk){
                bestAsk = dealerList.get(i).getAskPrices().get(0);
            }
        }

        return Math.max(0, bestAsk - bestBid);
    }
}