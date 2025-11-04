import React from 'react';
import DocumentProtection from './DocumentProtection';

/**
 * Wrapper pour appliquer la protection à n'importe quel composant
 */
const ProtectedWrapper = ({ children, documentTitle, showWatermark = true }) => {
  return (
    <DocumentProtection documentTitle={documentTitle} showWatermark={showWatermark}>
      {children}
    </DocumentProtection>
  );
};

export default ProtectedWrapper;
