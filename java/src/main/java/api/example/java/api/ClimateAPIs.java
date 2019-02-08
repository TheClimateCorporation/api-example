package api.example.java.api;

import java.util.Iterator;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;

import api.example.java.Config;
import api.example.java.model.ActivityResult;

@Component
public class ClimateAPIs {
    private static Logger logger = LoggerFactory.getLogger(ClimateAPIs.class);
    @Autowired
    protected RequestClient requestClient;
    @Autowired
    protected Config config;

    public Iterator<ActivityResult> getActivityIterator(String uri, String accessToken) {
        return new Iterator<ActivityResult>() {
            private boolean hasNext = true;
            private String xLimitValue = "30";
            private HttpHeaders responseHeaders = new HttpHeaders();
            private final String xNextToken = "x-next-token";
            private final String xLimit = "x-limit";

            @Override
            public boolean hasNext() {
                return hasNext;
            }

            @Override
            public ActivityResult next() {
                return requestClient.getWebClient(uri, accessToken, config.apiKey)
                        .get()
                        .header(xLimit, xLimitValue)
                        .header(xNextToken, nextTokenValue())
                        .exchange()
                        .doOnSuccess(clientResponse -> {
                            responseHeaders = clientResponse.headers().asHttpHeaders();
                            logger.info("Headers -> {}", responseHeaders);
                            logger.info("Status code -> {}", clientResponse.statusCode());
                            if (clientResponse.statusCode() == HttpStatus.PARTIAL_CONTENT
                                    || clientResponse.statusCode() == HttpStatus.OK) {
                                hasNext = true;
                            } else {
                                hasNext = false;
                            }
                        })
                        .flatMap(res -> res.bodyToMono(ActivityResult.class))
                        .block();
            }

            private String nextTokenValue() {
                List<String> headers = responseHeaders.get(this.xNextToken);
                return headers == null ? "" : headers.get(0);
            }
        };
    }

    public Iterator<ByteArrayResource> getContentIterator(String uri, Integer length, String accessToken) {
        return new Iterator<ByteArrayResource>() {
            private final int BUFFER_LEN = 1024 * 1024;
            private int currentLength = 0;

            @Override
            public boolean hasNext() {
                return currentLength < length;
            }

            @Override
            public ByteArrayResource next() {
                int start = currentLength;
                currentLength += BUFFER_LEN;
                return requestClient.getWebClient(uri, accessToken, config.apiKey)
                        .get()
                        .header(HttpHeaders.RANGE, String.format("bytes=%s-%s", start, currentLength - 1))
                        .retrieve()
                        .bodyToMono(ByteArrayResource.class)
                        .block();
            }
        };

    }
}
