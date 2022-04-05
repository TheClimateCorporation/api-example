package api.example.java.controllers;

import api.example.java.api.ClimateAPIs;
import api.example.java.model.HarvestReportsRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpServletRequest;

@Controller
public class HarvestReportsController extends BaseController {
    private static final String HARVESTREPORTS = "harvestReports";

    private static final String HARVESTREPORTS_PAGE = HARVESTREPORTS;

    private static final String HARVESTREPORTSCONTENTS = "harvestReportsContents";

    private static final String HARVESTREPORTSCONTENTS_PAGE = HARVESTREPORTSCONTENTS;

    @Autowired
    private ClimateAPIs climateAPIs;
    private static Logger logger = LoggerFactory.getLogger(GrowingSeasonsController.class);

    @GetMapping("/harvestReports")
    public String createHarvestReports() {
        logger.info("Get createHarvestReports entered");
        return HARVESTREPORTS_PAGE;
    }

    @PostMapping(value="/harvestReports", consumes=MediaType.APPLICATION_FORM_URLENCODED_VALUE)
    public String createHarvestReports(Model model, HttpServletRequest request, HarvestReportsRequest input) {
        logger.info("Post createHarvestReports entered");
        logger.info("FieldId entered is " + input.getFieldId());
        logger.info("GrowingSeasons entered is " + input.getGrowingSeasons());
        model.addAttribute(HARVESTREPORTS, climateAPIs.createHarvestReport(
                harvestReportsApiUri(), input, getAccessTokenFromSession(request)));
        return HARVESTREPORTS_PAGE;
    }

    @GetMapping("/harvestReportsContents/{id}")
    public String getHarvestReportsContents(Model model, HttpServletRequest request, @PathVariable String id) {
        logger.info("getHarvestReportsContents entered");
        logger.info("harvestReportsContentsId entered is " + id);
        model.addAttribute(HARVESTREPORTSCONTENTS, climateAPIs.getHarvestReportsContents(
                harvestReportsContentsApiUri(id), getAccessTokenFromSession(request)));
        return HARVESTREPORTSCONTENTS_PAGE;
    }

}
