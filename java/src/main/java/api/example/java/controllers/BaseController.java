package api.example.java.controllers;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import api.example.java.Config;
import api.example.java.model.TokenResponse;

public class BaseController {

	@Autowired
	protected Config config;

	public BaseController() {
	}

	protected String getAccessTokenFromSession(HttpServletRequest request) {
		TokenResponse tokenResponse = (TokenResponse) request.getSession().getAttribute("tokenResponse");
		return tokenResponse.getAccessToken();
	}

	protected boolean isUserLoggedIn(HttpSession session) {
		Object tokenResponse = session.getAttribute("tokenResponse");
		if (tokenResponse != null) {
			return true;
		}
	
		return false;
	}

	@ExceptionHandler(WebClientResponseException.class)
	public ResponseEntity<String> handleWebClientResponseException(WebClientResponseException ex) {
		return ResponseEntity.status(ex.getRawStatusCode()).body(ex.getResponseBodyAsString());
	}

	protected void saveTokenResponseInSession(HttpServletRequest request, TokenResponse tokenResponse) {
		request.getSession().setAttribute("tokenResponse", tokenResponse);
	}
	protected void cleanSession(HttpServletRequest request) {
		request.getSession().removeAttribute("tokenResponse");
		
	}	
	protected String agronomicApiUri() {
		return config.buildAgronomicApiUri();
	}
	protected String agronomicContentsApiUri(String id, String dataType) {
		return config.buildAgronomicContentsApiUri(id, dataType);
	}
}