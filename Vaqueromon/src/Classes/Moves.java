package Classes;
public enum  Moves {
     SCORCH_FANG, AQUA_SPIRAL , THORN_STRIKE;
     
     public String toString(){
        switch(this) {
            case SCORCH_FANG: return "Scorch Fang";
            case AQUA_SPIRAL: return "Aqua Spiral";
            case THORN_STRIKE: return "Thorn Strike";
            default: return "Unknown";
        }
    }
}
