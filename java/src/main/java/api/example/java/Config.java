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

	@Value("${CLIMATE_APP_ID}")
	public String appKey;

	@Value("${CLIMATE_APP_SECRET}")
	public String appSecret;

	@Value("${CLIMATE_API_KEY}")
	public String apiKey;

	@Value("${CLIMATE_API_SCOPES}")
	public String scopes;

	public Config() {
		if (StringUtils.isEmpty(System.getenv("CLIMATE_APP_ID"))) {
			throw new IllegalArgumentException("Please set environment variable CLIMATE_APP_ID");
		}
		if (StringUtils.isEmpty(System.getenv("CLIMATE_APP_SECRET"))) {
			throw new IllegalArgumentException("Please set environment variable CLIMATE_APP_SECRET");
		}
		if (StringUtils.isEmpty(System.getenv("CLIMATE_API_KEY"))) {
			throw new IllegalArgumentException("Please set environment variable CLIMATE_API_KEY");
		}
		if (StringUtils.isEmpty(System.getenv("CLIMATE_API_SCOPES"))) {
			throw new IllegalArgumentException("Please set environment variable CLIMATE_API_SCOPES");
		}
	}

	public String buildOauthLink(String server) {
		/*
		 * https://climate.com/static/app-login/index.html ?scope=${scope}
		 * &page=oidcauthn &response_type=code &redirect_uri=${redirect_uri}
		 * &client_id=${client_id}
		 */
		return UriComponentsBuilder.newInstance().scheme("https").host(loginServer).path(loginPath)
				.queryParam("page", "oidcauthn").queryParam("response_type", "code").queryParam("scope", scopes)
				.queryParam("client_id", appKey).queryParam("redirect_uri", server + "login-redirect").build()
				.toUriString();

	}

	public String buildTokenUri() {
		// https://api.climate.com/api/oauth/token
		return UriComponentsBuilder.newInstance().scheme("https").host(tokenServer).path(tokenPath).build().toString();
	}

	public String buildAgronomicApiUri() {
		// https://platform.climate.com/v4/layers
		return UriComponentsBuilder.newInstance().scheme("https").host(apiServer).path("/v4/layers").build().toString();

	}

	public String getBase64Credentials() {

		return "Basic " + new String(Base64Utils.encode((appKey + ":" + appSecret).getBytes()));
	}

	public String buildAgronomicContentsApiUri(String id, String dataType) {
		// https://platform.climate.com/v4/layers/id/contents
		return UriComponentsBuilder.newInstance().scheme("https").host(apiServer).path("/v4/layers/").path(dataType)
				.path("/").path(id).path("/contents").build().toString();
	}

}