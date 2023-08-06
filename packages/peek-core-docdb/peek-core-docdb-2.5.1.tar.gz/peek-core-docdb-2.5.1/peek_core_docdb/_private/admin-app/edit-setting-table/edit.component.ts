import { Component } from "@angular/core"
import { BalloonMsgService, NgLifeCycleEvents } from "@synerty/peek-plugin-base-js"
import { extend, TupleLoader, VortexService } from "@synerty/vortexjs"
import { docDbFilt, SettingPropertyTuple } from "@peek/peek_core_docdb/_private"

@Component({
    selector: "pl-docdb-edit-setting",
    templateUrl: "./edit.component.html"
})
export class EditSettingComponent extends NgLifeCycleEvents {
    items: SettingPropertyTuple[] = []
    loader: TupleLoader
    
    // This must match the dict defined in the admin_backend handler
    private readonly filt = {
        "key": "admin.Edit.SettingProperty"
    }
    
    constructor(
        private balloonMsg: BalloonMsgService,
        vortexService: VortexService
    ) {
        super()
        
        this.loader = vortexService.createTupleLoader(this,
            () => extend({}, this.filt, docDbFilt))
        
        this.loader.observable
            .subscribe((tuples: SettingPropertyTuple[]) => this.items = tuples)
    }
    
    saveClicked() {
        this.loader.save()
            .then(() => this.balloonMsg.showSuccess("Save Successful"))
            .catch(e => this.balloonMsg.showError(e))
    }
    
    resetClicked() {
        this.loader.load()
            .then(() => this.balloonMsg.showSuccess("Reset Successful"))
            .catch(e => this.balloonMsg.showError(e))
    }
    
}
