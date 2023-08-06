

from aiida.engine import WorkChain
from aiida.orm import Float, Dict
from aiida.plugins import WorkflowFactory, Datafactory

StructureData = Datafactory('structure') #pylint: disable=invalid-name
OrcaBaseWorkChain = WorkflowFactory('orca.base') #pylint: disable=invalid-name

class OrcaRelaxWorkChain(WorkChain):

    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.expose_inputs(OrcaBaseWorkChain, namespace='orca')
        spec.input(structure, valid_type=StructureData, require=True, help='Structure object to run the calculations.')
        spec.input('force_threshold', required=True, default=lambda: Float(0.1))

        spec.outline(
            cls.initialize,
            cls.run_relax,
            cls.results
        )

        # Exit codes

        # Register outputs
        spec.output('output_parameters', valid_type=Dict, required=True, help='relaxed structure')

    
    def initialize(self):
        return
    
    def run_relax(self):
        return
    
    def results(self):
        return

#EOF

