


import java.math.BigDecimal;


public class MetodosMM {
    public static BigDecimal serviceTime (double tiempoCola, double medServicio){
        BigDecimal serviceTime = new BigDecimal(tiempoCola).add(new BigDecimal(medServicio));
        return serviceTime;
    }
    
    public static BigDecimal clientsInLine (double medLlegada, double tiempoCola){
        BigDecimal clientsInLine = new BigDecimal(medLlegada).multiply(new BigDecimal(tiempoCola));
        return clientsInLine;
    }
    
    public static BigDecimal clientsInSystem (double medLlegada, double tiempoServicio) {
        BigDecimal clientsInSystem = new BigDecimal(medLlegada).multiply(new BigDecimal(tiempoServicio));
        return clientsInSystem;
    }
    
    public static BigDecimal probOcupado (double medLlegada, double medServicio){
        BigDecimal probOcupado = new BigDecimal(medLlegada).divide(new BigDecimal(medServicio));
        return probOcupado;
    }
    
    public static BigDecimal probOcio (double medLlegada, double medServicio){
        BigDecimal probOcio = BigDecimal.ONE.subtract(new BigDecimal(medLlegada).divide(new BigDecimal(medServicio)));
        return probOcio;
    }
    
    public static BigDecimal probN (double medLlegada, double medServicio, int n){
        BigDecimal division = new BigDecimal (medLlegada).divide(new BigDecimal (medServicio));
        BigDecimal resta = BigDecimal.ONE.subtract(division);
        BigDecimal elevado = division.pow(n);
        BigDecimal resultado = resta.multiply(elevado);
        return resultado;
    }
    
    public static BigDecimal clientesCola(double medLlegada, double tiempoCola) {
        BigDecimal resultado = new BigDecimal(medLlegada).multiply(new BigDecimal(tiempoCola));
        return resultado;
    }
    
}