package api.example.java;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.Base64Utils;
import org.springframework.util.StringUtils;
import org.springframework.web.util.UriComponentsBuilder;

@Configuration
public class Config {
    @Value("${climate.login.server}")
    public String loginServer;

    @Value("${climate.login.path}")
    public String loginPath;

    @Value("${climate.token.server}")
    public String tokenServer;

    @Value("${climate.token.path}")
    public String tokenPath;

    @Value("${climate.api.server}")
    public String apiServer;

    @Value("${CLIENT_ID}")
    public String clientId;

    @Value("${CLIENT_SECRET}")
    public String clientSecret;

    @Value("${API_KEY}")
    public String apiKey;

    @Value("${API_SCOPES}")
    public String scopes;

    public Config() {
        if (StringUtils.isEmpty(System.getenv("CLIENT_ID"))) {
            throw new IllegalArgumentException("Please set environment variable CLIENT_ID");
        }
        if (StringUtils.isEmpty(System.getenv("CLIENT_SECRET"))) {
            throw new IllegalArgumentException("Please set environment variable CLIENT_SECRET");
        }
        if (StringUtils.isEmpty(System.getenv("API_KEY"))) {
            throw new IllegalArgumentException("Please set environment variable API_KEY");
        }
        if (StringUtils.isEmpty(System.getenv("API_SCOPES"))) {
            throw new IllegalArgumentException("Please set environment variable API_SCOPES");
        }
    }

    public String buildOauthLink(String redirectUri) {
        /*
         * https://climate.com/static/app-login/index.html?scope=${scope}
         * &page=oidcauthn&response_type=code&redirect_uri=${redirect_uri}
         * &client_id=${client_id}
         */
        return UriComponentsBuilder
                .newInstance()
                .scheme("https")
                .host(loginServer)
                .path(loginPath)
                .queryParam("page", "oidcauthn")
                .queryParam("response_type", "code")
                .queryParam("scope", scopes)
                .queryParam("client_id", clientId)
                .queryParam("redirect_uri", redirectUri)
                .build()
                .toUriString();
    }

    public String buildTokenUri() {
        // https://api.climate.com/api/oauth/token
        return getUriComponentsBuilder(tokenServer, tokenPath);
    }

    public String buildAgronomicApiUri(String dataType) {
        // https://platform.climate.com/v4/layers
        return getUriComponentsBuilder(apiServer, "/v4/layers/" + dataType);
    }

    public String getBase64Credentials() {
        return "Basic " + new String(Base64Utils.encode((clientId + ":" + clientSecret).getBytes()));
    }

    public String buildAgronomicContentsApiUri(String id, String dataType) {
        // https://platform.climate.com/v4/layers/id/contents
        return getUriComponentsBuilder(apiServer, String.format("/v4/layers/%s/%s/contents", dataType, id));
    }

    private String getUriComponentsBuilder(String host, String path) {
        return UriComponentsBuilder.newInstance()
                .scheme("https")
                .host(host)
                .path(path)
                .build()
                .toString();
    }

}