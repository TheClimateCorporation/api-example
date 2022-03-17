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
    protected static final String LOGIN_REDIRECT = "login-redirect";
    protected static final String HOME_PAGE = "home";
    protected static final String INDEX_PAGE = "index";
    protected static final String REDIRECT_TO_HOME_PAGE = "redirect:/";
    protected static final String TOKEN_RESPONSE = "tokenResponse";
    protected static final String CODE = "code";
    protected static final String REFRESH_TOKEN = "refresh_token";
    @Autowired
    protected Config config;

    protected String getAccessTokenFromSession(HttpServletRequest request) {
        String token = "";
        if (request.getSession().getAttribute(TOKEN_RESPONSE) instanceof TokenResponse) {
            TokenResponse tokenResponse = (TokenResponse) request.getSession().getAttribute(TOKEN_RESPONSE);
            token = tokenResponse.getAccessToken();
        }
        return token;
    }

    protected boolean isUserLoggedIn(HttpSession session) {
        return session.getAttribute(TOKEN_RESPONSE) != null;
    }

    @ExceptionHandler(WebClientResponseException.class)
    public ResponseEntity<String> handleWebClientResponseException(WebClientResponseException ex) {
        return ResponseEntity.status(ex.getRawStatusCode()).body(ex.getResponseBodyAsString());
    }

    protected void saveTokenResponseInSession(HttpServletRequest request, TokenResponse tokenResponse) {
        request.getSession().setAttribute(TOKEN_RESPONSE, tokenResponse);
    }

    protected void cleanSession(HttpServletRequest request) {
        request.getSession().removeAttribute(TOKEN_RESPONSE);
    }

    protected String agronomicApiUri(String dataType) {
        return config.buildAgronomicApiUri(dataType);
    }

    protected String agronomicContentsApiUri(String id, String dataType) {
        return config.buildAgronomicContentsApiUri(id, dataType);
    }

    protected String fieldsApiUri() {
        return config.buildFieldsApiUri();
    }
}
