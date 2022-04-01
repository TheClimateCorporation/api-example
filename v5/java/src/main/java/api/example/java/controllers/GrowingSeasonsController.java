package api.example.java.controllers;

import javax.servlet.http.HttpServletRequest;

import api.example.java.model.Field;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

import api.example.java.api.ClimateAPIs;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@Controller
public class GrowingSeasonsController extends BaseController {

    private static final String GROWINGSEASONS = "growingSeasons";

    private static final String GROWINGSEASONS_PAGE = GROWINGSEASONS;

    private static final String GROWINGSEASONSCONTENTS = "growingSeasonsContents";

    private static final String GROWINGSEASONSCONTENTS_PAGE = GROWINGSEASONSCONTENTS;
    @Autowired
    private ClimateAPIs climateAPIs;
    private static Logger logger = LoggerFactory.getLogger(GrowingSeasonsController.class);

    @GetMapping("/growingSeasons")
    public String createGrowingSeasons() {
        logger.info("Get createGrowingSeasons entered");
        return GROWINGSEASONS_PAGE;
    }

    @PostMapping(value="/growingSeasons", consumes=MediaType.APPLICATION_FORM_URLENCODED_VALUE)
    public String createGrowingSeasons(Model model, HttpServletRequest request, Field fieldId) {
        logger.info("Post createGrowingSeasons entered");
        logger.info("FieldId entered is " + fieldId.getFieldId());
        model.addAttribute(GROWINGSEASONS, climateAPIs.createGrowingSeasons(growingSeasonsApiUri(), fieldId.getFieldId(), getAccessTokenFromSession(request)));
        return GROWINGSEASONS_PAGE;
    }

    @GetMapping("/growingSeasonsContents/{id}")
    public String getGrowingSeasonsContents(Model model, HttpServletRequest request, @PathVariable String id) {
        logger.info("Post createGrowingSeasonsContents entered");
        logger.info("growingSeasonsContentsId entered is " + id);
        model.addAttribute(GROWINGSEASONSCONTENTS, climateAPIs.getGrowingSeasonsContents(growingSeasonsContentsApiUri(id), getAccessTokenFromSession(request)));
        logger.info(GROWINGSEASONSCONTENTS);
        return GROWINGSEASONSCONTENTS_PAGE;
    }
}
