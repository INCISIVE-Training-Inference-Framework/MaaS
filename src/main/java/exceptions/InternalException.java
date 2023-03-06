package exceptions;

import org.apache.logging.log4j.Logger;

public class InternalException extends Exception {

    private static final String topic = "Internal exception: ";
    private final Exception exception;

    public InternalException(String errorMessage, Exception exception) {
        super(topic + errorMessage);
        this.exception = exception;
    }

    public Exception getException() {
        return exception;
    }

    public void print(Logger logger) {
        logger.error(this.getMessage());
        if (this.getException() != null) {
            logger.error(this.getException().getMessage());
            this.getException().printStackTrace();
        }
    }
}