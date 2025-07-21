import { ReactNode, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion } from 'framer-motion';

export interface ModalProps {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}

export default function Modal({ open, onClose, children }: ModalProps) {
  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
    }
    if (open) document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [open, onClose]);

  if (!open) return null;
  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={onClose}
      aria-modal="true"
      role="dialog"
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-white p-4 rounded-2xl dark:bg-gray-800"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="float-right" aria-label="Close" onClick={onClose}>
          &times;
        </button>
        {children}
      </motion.div>
    </div>,
    document.body
  );
}
