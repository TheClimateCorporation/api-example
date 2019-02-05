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

	public Iterator<ActivityResult> getActivityIterator(String uri, String dataType, String accessToken) {

		return new Iterator<ActivityResult>() {
			private boolean hasNext = true;
			private String xLimitValue = "30";
			private HttpHeaders responseHeader = new HttpHeaders();
			private final String xNextToken = "x-next-token";
			private final String xLimt = "x-limit";

			@Override
			public boolean hasNext() {
				return hasNext;
			}

			@Override
			public ActivityResult next() {
				return requestClient.getWebClient(uri, accessToken, config.apiKey).get().header(xLimt, xLimitValue)
						.header(xNextToken, nextTokenValue()).exchange().doOnSuccess(clientResponse -> {
							responseHeader = clientResponse.headers().asHttpHeaders();
							logger.info("Headers -> {}", responseHeader);
							logger.info("Status code -> {}", clientResponse.statusCode());
							if (clientResponse.statusCode() == HttpStatus.PARTIAL_CONTENT
									|| clientResponse.statusCode() == HttpStatus.OK) {
								hasNext = true;
							} else {
								hasNext = false;
							}
						}).flatMap(res -> res.bodyToMono(ActivityResult.class)).block();
			}

			private String nextTokenValue() {
				String xNextToken;
				List<String> headers = responseHeader.get(this.xNextToken);
				if (headers == null) {
					xNextToken = "";
				} else {
					xNextToken = headers.get(0);
				}
				return xNextToken;
			}
		};
	}

	public Iterator<ByteArrayResource> getContentIterator(String uri, String dataType, String id, Integer length,
			String accessToken) {

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
				return requestClient.getWebClient(uri, accessToken, config.apiKey).get()
						.header("Range", String.format("bytes=%s-%s", start, currentLength - 1)).retrieve()
						.bodyToMono(ByteArrayResource.class).block();
			}
		};

	}
}
