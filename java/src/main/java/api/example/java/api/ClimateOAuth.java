package api.example.java.api;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.BodyInserters;

import api.example.java.Config;
import api.example.java.model.TokenResponse;

@Component
public class ClimateOAuth {

    @Autowired
    private Config config;

    @Autowired
    private RequestClient requestClient;

    private static Logger logger = LoggerFactory.getLogger(ClimateOAuth.class);

    public TokenResponse getToken(String code, String redirectUri) {

        // grant_type=authorization_code&redirect_uri=${redirect_uri}&code=${code}
        MultiValueMap<String, String> formData = new LinkedMultiValueMap<String, String>();
        formData.add("code", code);
        formData.add("grant_type", "authorization_code");
        formData.add("redirect_uri", redirectUri);

        logger.info("Request body value map: {}", formData.toString());

        return makeRequest(formData);
    }

    private TokenResponse makeRequest(MultiValueMap<String, String> formData) {
        TokenResponse tokenResponse = requestClient.getWebClient(config.buildTokenUri(), config.getBase64Credentials())
                .post()
                .body(BodyInserters.fromFormData(formData))
                .retrieve().bodyToMono(TokenResponse.class)
                .block();
        return tokenResponse;
    }

    public TokenResponse getRefreshToken(String refreshToken) {

        // grant_type=authorization_code&redirect_uri=${redirect_uri}&code=${code}
        MultiValueMap<String, String> formData = new LinkedMultiValueMap<String, String>();
        formData.add("refresh_token", refreshToken);
        formData.add("grant_type", "refresh_token");

        logger.info("Request body value map: {}", formData.toString());

        return makeRequest(formData);
    }

}
